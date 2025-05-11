from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Product, Cart, CartItem, Order, OrderItem, UserProfile, PhoneVerification, generate_username, OTP
from decimal import Decimal
from django.contrib.auth.models import User
import requests
import json
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

# Create your views here.

def send_otp(phone_number):
    print(phone_number)
    data = {'to': phone_number}
    response = requests.post('https://console.melipayamak.com/api/send/otp/c17b71e07b2a4411bd29999ec6696e29', json=data)
    return response.json()


def home_view(request):
    products = Product.objects.all()
    cart_items = []
    cart_items_count = 0
    
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart__user=request.user)
        cart_items_count = cart_items.count()
    
    context = {
        'products': products,
        'cart_items': cart_items,
        'cart_items_count': cart_items_count,
    }
    return render(request, 'accounts/home.html', context)

def send_verification_email(user, request):
    print("\n=== Starting Email Verification Process ===")
    print(f"User email: {user.email}")
    print(f"User username: {user.username}")
    
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_url = request.build_absolute_uri(f'/accounts/verify-email/{uid}/{token}/')
    print(f"Generated verification URL: {verification_url}")
    
    subject = 'تایید ایمیل شما در پایمونک'
    print(f"Email subject: {subject}")
    
    try:
        message = render_to_string('accounts/email/verify_email.html', {
            'user': user,
            'verification_url': verification_url,
        })
        message = "Verify URLS IS : " + verification_url
        print("Email template rendered successfully")
    except Exception as e:
        print(f"Error rendering template: {str(e)}")
        raise e
    
    print("\nEmail Settings:")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
    print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    print("\nAttempting to send email...")
    try:
        result = send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            auth_user=settings.EMAIL_HOST_USER,
            auth_password=settings.EMAIL_HOST_PASSWORD,
            fail_silently=False,
        )
        print(f"Email send result: {result}")
        
        if result == 0:
            print("Warning: No emails were sent!")
            
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        print(f"Error type: {type(e)}")
        print(f"Error details: {str(e)}")
        raise e
        
    print("=== Email Verification Process Complete ===\n")

def verify_emailX(request):
    return redirect("home")

def verify_email(request, uidb64, token):
    print("We have reached verify email")
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.profile.is_email_verified = True
        user.profile.save()
        messages.success(request, 'ایمیل شما با موفقیت تایید شد')
        return redirect('login')
    else:
        messages.error(request, 'لینک تایید نامعتبر است یا منقضی شده است')
        return redirect('login')

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(f'/password-reset/{uid}/{token}/')
            
            subject = 'بازیابی رمز عبور در پایمونک'
            message = render_to_string('accounts/email/password_reset_email.html', {
                'user': user,
                'reset_url': reset_url,
            })
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            messages.success(request, 'لینک بازیابی رمز عبور به ایمیل شما ارسال شد')
        except User.DoesNotExist:
            messages.error(request, 'کاربری با این ایمیل یافت نشد')
        return redirect('login')
    
    return render(request, 'accounts/password_reset_request.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'رمز عبور شما با موفقیت تغییر کرد')
                return redirect('login')
            else:
                messages.error(request, 'رمز عبور و تکرار آن مطابقت ندارند')
    else:
        messages.error(request, 'لینک بازیابی نامعتبر است یا منقضی شده است')
        return redirect('login')
    
    return render(request, 'accounts/password_reset_confirm.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        registration_type = request.POST.get('registration_type')

        if registration_type == 'email':
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')

            # Check for unique username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'نام کاربری قبلا انتخاب شده است')
                return redirect('register')

            # Check for unique email
            if User.objects.filter(email=email).exists():
                messages.error(request, 'این ایمیل قبلاً ثبت شده است')
                return redirect('register')

            try:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.profile.phone_number = None
                user.profile.save()
                
                # Send verification email
                try:
                    send_verification_email(user, request)
                    messages.success(request, 'ثبت نام شما با موفقیت انجام شد. لطفاً ایمیل خود را برای تایید بررسی کنید.')
                except Exception as e:
                    messages.warning(request, 'ثبت نام انجام شد اما در ارسال ایمیل تایید مشکلی پیش آمده است.')
                
                login(request, user)
                return redirect('home')
            except Exception as e:
                messages.error(request, 'خطا در ثبت نام. لطفاً دوباره تلاش کنید.')
                return redirect('register')

        else:  # Phone registration
            phone = request.POST.get('phone')
            password = request.POST.get('password')

            print(f"Debug - Received phone: {phone}")  # Debug log

            if not phone or not phone.isdigit() or len(phone) != 11:
                messages.error(request, 'شماره تلفن نامعتبر است')
                return redirect('register')

            if UserProfile.objects.filter(phone_number=phone).exists():
                messages.error(request, 'شماره تلفن قبلا استفاده شده است')
                return redirect('register')

            # Store registration data in session
            request.session['registration_phone'] = phone
            request.session['registration_password'] = password
            request.session.modified = True  # Ensure session is saved

            print(f"Debug - Session data after setting: {request.session.items()}")  # Debug log

            # Send OTP
            response = send_otp(phone)
            print(f"Debug - OTP response: {response}")  # Debug log
            
            if 'code' in response:
                PhoneVerification.objects.create(
                    phone_number=phone,
                    code=response['code']
                )
                messages.success(request, response['status'])
                return redirect('verify_phone_register')
            else:
                messages.error(request, 'خطا در ارسال کد تایید')
                return redirect('register')

    return render(request, 'accounts/register.html')

def verify_phone_register(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        phone = request.session.get('registration_phone')
        password = request.session.get('registration_password')

        print(f"Debug - Phone from session: {phone}")  # Debug log
        print(f"Debug - Code received: {code}")  # Debug log
        print(f"Debug - Full session data: {request.session.items()}")  # Debug log

        if not phone or not password:
            messages.error(request, 'اطلاعات ثبت نام نامعتبر است')
            return redirect('register')

        verification = PhoneVerification.objects.filter(
            phone_number=phone,
            code=code,
            is_used=False,
            created_at__gte=timezone.now() - timedelta(minutes=5)
        ).first()
        
        if verification:
            verification.is_used = True
            verification.save()
            
            # Generate unique username
            username = generate_username(phone)
            user = User.objects.create_user(username=username, password=password)
            user.profile.is_phone_verified = True
            user.profile.phone_number = phone
            user.profile.save()

            # Clear session data
            del request.session['registration_phone']
            del request.session['registration_password']
            request.session.modified = True  # Ensure session is saved

            login(request, user)
            messages.success(request, 'ثبت نام شما با موفقیت انجام شد')
            return redirect('home')
        else:
            messages.error(request, 'کد وارد شده اشتباه است یا منقضی شده است')
            # Resend OTP
            response = send_otp(phone)
            if 'code' in response:
                PhoneVerification.objects.create(
                    phone_number=phone,
                    code=response['code']
                )
                messages.success(request, response['status'])
    
    return render(request, 'accounts/verify_phone_register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        login_type = request.POST.get('login_type')
        password = request.POST.get('password')
        
        if login_type == 'email':
            username = request.POST.get('username')
            user = authenticate(request, username=username, password=password)
        else:  # phone login
            phone = request.POST.get('phone')
            try:
                user_profile = UserProfile.objects.get(phone_number=phone)
                user = authenticate(request, username=user_profile.user.username, password=password)
            except UserProfile.DoesNotExist:
                user = None
        
        if user is not None:
            login(request, user)
            messages.success(request, 'شما با موفقیت وارد شدید')
            return redirect('home')
        else:
            messages.error(request, 'اطلاعات وارد شده اشتباه است')
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'شما با موفقیت خارج شدید')
        return redirect('login')
    return redirect('home')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'accounts/product_list.html', {'products': products})

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    cart_total = cart.get_total()
    return render(request, 'accounts/cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'cart_total': cart_total
    })

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        messages.success(request, f'{product.name} به سبد خرید شما اضافه شد')
        return redirect('cart')
    return redirect('product_list')

@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        cart_item = CartItem.objects.filter(id=item_id, cart__user=request.user).first()
        if cart_item:
            cart_item.delete()
            messages.success(request, 'آیتم از سبد خرید شما حذف شد')
        else:
            messages.warning(request, 'ایتمی در سبد خرید شما یافت نشد')
        return redirect('cart')
    return redirect('cart')

@login_required
def update_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'سبد خرید شما با موفقیت به روز شد')
        else:
            cart_item.delete()
            messages.success(request, 'آیتم از سبد خرید شما حذف شد')
            
        return redirect('cart')
    return redirect('cart')

@login_required
def verify_phone(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        verification = PhoneVerification.objects.filter(
            phone_number=request.user.profile.phone_number,
            code=code,
            is_used=False,
            created_at__gte=timezone.now() - timedelta(minutes=5)
        ).first()
        
        if verification:
            verification.is_used = True
            verification.save()
            request.user.profile.is_phone_verified = True
            request.user.profile.save()
            messages.success(request, 'شماره تلفن شما با موفقیت تایید شد')
            return redirect('home')
        else:
            messages.error(request, 'کد وارد شده اشتباه است یا منقضی شده است')
    
    # Send new OTP
    if not request.user.profile.is_phone_verified:
        response = send_otp(request.user.profile.phone_number)
        print("RESPONSE::"+str(response))
        if 'code' in response:
            PhoneVerification.objects.create(
                phone_number=request.user.profile.phone_number,
                code=response['code']
            )
            messages.success(request, response['status'])
    
    return render(request, 'accounts/verify_phone.html')

@login_required
def profile_view(request):
    print("\n=== Profile View Accessed ===")
    if request.method == 'POST':
        action = request.POST.get('action')
        print(f"POST action received: {action}")
        
        if action == 'update_email':
            email = request.POST.get('email')
            if email != request.user.email:
                request.user.email = email
                request.user.profile.is_email_verified = False
                request.user.save()
                messages.success(request, 'ایمیل شما با موفقیت به روز شد')
                return redirect('profile')
            
        elif action == 'verify_email':
            print("Email verification requested")
            if not request.user.profile.is_email_verified:
                print("User email not verified, sending verification email...")
                send_verification_email(request.user, request)
                messages.success(request, 'لینک تایید ایمیل به آدرس ایمیل شما ارسال شد')
            else:
                print("User email is already verified")
                messages.info(request, 'ایمیل شما قبلاً تایید شده است')
            return redirect('profile')
                
        elif action == 'update_phone':
            phone = request.POST.get('phone')
            if(phone != ""):
                if UserProfile.objects.filter(phone_number=phone).exclude(user=request.user).exists():
                    messages.error(request, 'شماره تلفن قبلا انتخاب شده است')
                else:
                    request.user.profile.phone_number = phone
                    request.user.profile.is_phone_verified = False
                    request.user.profile.save()
                    messages.success(request, 'شماره تلفن شما با موفقیت به روز شد لطفا شماره خود را تایید کنید')
                    return redirect('verify_phone')
                
        elif action == 'update_password':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            if request.user.check_password(old_password):
                request.user.set_password(new_password)
                request.user.save()
                messages.success(request, 'پسورد شما با موفقیت به روز شد')
                return redirect('login')
            else:
                messages.error(request, 'پسورد فعلی اشتباه است')
                
        elif action == 'update_image':
            if 'profile_image' in request.FILES:
                request.user.profile.profile_image = request.FILES['profile_image']
                request.user.profile.save()
                messages.success(request, 'عکس پروفایل شما با موفقیت به روز شد')
    
    return render(request, 'accounts/profile.html')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    if not request.user.profile.phone_number:
        messages.error(request, 'لطفا شماره تلفن خود را وارد کنید')
        return redirect('profile')
    
    if not request.user.profile.is_phone_verified:
        messages.error(request, 'لطفا قبل خرید شماره تلفن خود را تایید کنید')
        return redirect('verify_phone')
    
    if request.method == 'POST':
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=cart.get_total()
        )
        
        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
        
        # Clear cart
        cart.items.all().delete()
        messages.success(request, 'خرید شما با موفقیت ثبت شد')
        return redirect('order_history')
    
    return render(request, 'accounts/checkout.html', {'cart': cart})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/order_history.html', {'orders': orders})
