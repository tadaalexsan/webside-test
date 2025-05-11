import React, { useState } from "react";
import { Avatar } from "../../components/ui/avatar";
import { Card, CardContent } from "../../components/ui/card";
import { Separator } from "../../components/ui/separator";
import { LoginModal } from "../../components/LoginModal";
import { ProductModal } from "../../components/ProductModal";

export const Screen = (): JSX.Element => {
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState<null | { name: string; price: string }>(null);
  
  const contactInfo = [
    { id: 1, platform: "تلگرام", handle: "@Paimonak" },
    { id: 2, platform: "تلگرام", handle: "@Paimonak" },
  ];

  const products = [
    {
      id: 1,
      name: "ولکین مون",
      price: "۴۰۰,۰۰۰ تومان",
      image: "/-----.png",
    },
    {
      id: 2,
      name: "ولکین مون",
      price: "۴۰۰,۰۰۰ تومان",
      image: "/------1.png",
    },
  ];

  const handleProductClick = (product: { name: string; price: string }) => {
    setSelectedProduct(product);
  };

  return (
    <div className="bg-[#f0eae4] min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex justify-between items-center py-4 sm:py-6">
          <div className="flex items-center space-x-4">
            <Avatar 
              className="w-8 h-8 sm:w-10 sm:h-10 bg-[#586070] cursor-pointer"
              onClick={() => setIsLoginOpen(true)}
            />
            <span className="text-base sm:text-lg [font-family:'HYWenHei-HEW',Helvetica] font-normal text-[#586070]">
              Alex
            </span>
            <div className="h-6 w-px bg-[#586070]" />
            <div className="relative">
              <div className="w-6 h-6 sm:w-8 sm:h-8 bg-[url(/huge-icon-ecommerce-outline-bag-01.svg)] bg-contain bg-no-repeat">
                <div className="absolute -top-1 -right-1 w-4 h-4 bg-x rounded-full flex items-center justify-center">
                  <span className="text-[10px] text-[#f0eae4] font-medium">۲</span>
                </div>
              </div>
            </div>
          </div>
          <img className="w-6 h-6 sm:w-8 sm:h-8" alt="Menu" src="/-----------.svg" />
        </div>

        {/* Banner */}
        <div className="mt-6 sm:mt-8">
          <img
            className="w-full h-auto rounded-lg object-cover"
            alt="Banner"
            src="/untitled-1banner-1.png"
          />
        </div>

        {/* What is Paimonak Section */}
        <section className="mt-12 sm:mt-16">
          <div className="text-center">
            <h1 className="text-2xl sm:text-3xl lg:text-4xl [font-family:'Yekan_Bakh-ExtraBold',Helvetica] font-extrabold text-[#586070]">
              پایمونک چیه؟
            </h1>
            <div className="mt-2 text-xl sm:text-2xl [font-family:'HYWenHei-HEW',Helvetica] bg-gradient-to-b from-[#586070] to-transparent bg-clip-text text-transparent">
              Paimonak
            </div>
          </div>
        </section>

        {/* Profile Creation Section */}
        <section className="mt-12 sm:mt-16">
          <h2 className="text-2xl sm:text-3xl text-center [font-family:'Yekan_Bakh-ExtraBold',Helvetica] font-extrabold text-[#586070]">
            ساخت پروفایل
          </h2>
          <p className="mt-4 text-base sm:text-lg text-justify [font-family:'Yekan_Bakh-SemiBold',Helvetica] text-[#586070]">
            میتونی پروفایل مخصوص خودتو داشته باشی، باهاش مشخصات کاراکتراتو ببینی و به بقیه نشون بدی!
          </p>
          <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-6">
            <img
              className="w-full h-auto rounded-lg"
              alt="Profile Preview"
              src="/untitled-1-imgid38-1.png"
            />
            <img
              className="w-full h-auto rounded-lg"
              alt="Profile Preview"
              src="/untitled-1-imgid38-1.png"
            />
          </div>
        </section>

        {/* Products Grid */}
        <section className="mt-12 sm:mt-16">
          <h2 className="text-2xl sm:text-3xl text-center [font-family:'Yekan_Bakh-ExtraBold',Helvetica] font-extrabold text-[#586070]">
            محصولات گنشین ایمپکت
          </h2>
          <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {products.map((product) => (
              <Card 
                key={product.id} 
                className="bg-x rounded-2xl transform transition hover:scale-105 cursor-pointer"
                onClick={() => handleProductClick(product)}
              >
                <CardContent className="p-4">
                  <img
                    className="w-full h-auto rounded-lg"
                    alt={product.name}
                    src={product.image}
                  />
                  <h3 className="mt-4 text-lg font-semibold text-center text-[#586070]">
                    {product.name}
                  </h3>
                  <p className="mt-2 text-center font-bold text-[#586070]">
                    قیمت: {product.price}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>

        <Separator className="my-12" />

        {/* Footer */}
        <footer className="py-8">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="text-center sm:text-right">
              <h3 className="text-xl font-bold text-[#586070]">پایمونک</h3>
              <div className="mt-4 space-y-2">
                {contactInfo.map((contact) => (
                  <div key={contact.id} className="flex items-center justify-end space-x-2">
                    <span className="text-[#586070]">{contact.handle}</span>
                    <span className="text-[#586070]">{contact.platform}</span>
                    <img className="w-5 h-5" alt="Telegram" src="/------------.svg" />
                  </div>
                ))}
              </div>
            </div>

            <div className="text-center">
              <div className="w-32 h-32 mx-auto bg-x rounded-xl" />
            </div>

            <div className="text-center sm:text-left">
              <h3 className="text-xl font-bold text-[#586070]">Contact Us</h3>
              <div className="mt-4 space-y-2">
                {contactInfo.map((contact) => (
                  <div key={contact.id} className="flex items-center space-x-2">
                    <img className="w-5 h-5" alt="Telegram" src="/------------.svg" />
                    <span className="text-[#586070]">Telegram: {contact.handle}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="mt-8 text-center text-sm text-[#586070]">
            تمامی حقوق برای مجموعه ویویل محفوظ میباشد.
          </div>
        </footer>
      </div>
      
      <LoginModal 
        isOpen={isLoginOpen}
        onClose={() => setIsLoginOpen(false)}
      />

      {selectedProduct && (
        <ProductModal
          isOpen={!!selectedProduct}
          onClose={() => setSelectedProduct(null)}
          product={selectedProduct}
        />
      )}
    </div>
  );
};