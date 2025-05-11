from .models import UserProfile

def create_user_profile(backend, user, response, *args, **kwargs):
    """Create user profile for social auth users if it doesn't exist."""
    if not hasattr(user, 'profile'):
        UserProfile.objects.create(user=user)
    return None 