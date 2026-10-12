from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

class TimeStamped(models.Model):
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: abstract=True
class Category(TimeStamped):
    title=models.CharField('نام دسته',max_length=100); slug=models.SlugField(unique=True, blank=True); description=models.TextField(blank=True); image=models.ImageField(upload_to='categories/',blank=True); active=models.BooleanField(default=True)
    class Meta: verbose_name='دسته‌بندی'; verbose_name_plural='دسته‌بندی‌ها'
    def save(self,*a,**k):
        if not self.slug: self.slug=slugify(self.title,allow_unicode=True)
        super().save(*a,**k)
    def __str__(self): return self.title
class Product(TimeStamped):
    category=models.ForeignKey(Category,on_delete=models.PROTECT,related_name='products',verbose_name='دسته‌بندی'); title=models.CharField(max_length=180); slug=models.SlugField(unique=True,blank=True); short_description=models.CharField(max_length=220,blank=True); description=models.TextField(blank=True); price=models.PositiveIntegerField('قیمت (تومان)'); compare_at_price=models.PositiveIntegerField('قیمت قبل',null=True,blank=True); stock=models.PositiveIntegerField(default=0); is_active=models.BooleanField(default=True); is_featured=models.BooleanField('پیشنهاد ویژه',default=False); is_new=models.BooleanField('محصول جدید',default=True); image=models.ImageField(upload_to='products/',blank=True); attributes=models.JSONField(default=dict,blank=True)
    class Meta: verbose_name='محصول'; verbose_name_plural='محصولات'; ordering=['-created_at']
    def save(self,*a,**k):
        if not self.slug: self.slug=slugify(self.title,allow_unicode=True)
        super().save(*a,**k)
    @property
    def discount_percent(self): return int((1-self.price/self.compare_at_price)*100) if self.compare_at_price else 0
    def __str__(self): return self.title
class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='gallery'); image=models.ImageField(upload_to='products/gallery/'); alt=models.CharField(max_length=120,blank=True)
    class Meta: verbose_name='تصویر محصول'; verbose_name_plural='گالری محصول'
class Variant(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='variants'); name=models.CharField(max_length=80); color=models.CharField(max_length=40,blank=True); size=models.CharField(max_length=30,blank=True); stock=models.PositiveIntegerField(default=0); extra_price=models.IntegerField(default=0)
    class Meta: verbose_name='تنوع'; verbose_name_plural='رنگ و سایز'
    def __str__(self): return f'{self.product} | {self.name}'
class Coupon(models.Model):
    code=models.CharField(max_length=30,unique=True); percent=models.PositiveSmallIntegerField(); active=models.BooleanField(default=True); expires_at=models.DateTimeField(null=True,blank=True)
    class Meta: verbose_name='کوپن'; verbose_name_plural='کوپن‌ها'
class Cart(TimeStamped):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True,related_name='cart'); session_key=models.CharField(max_length=40,null=True,blank=True,unique=True); coupon=models.ForeignKey(Coupon,null=True,blank=True,on_delete=models.SET_NULL)
    class Meta: verbose_name='سبد خرید'; verbose_name_plural='سبدهای خرید'
    @property
    def subtotal(self): return sum(i.total for i in self.items.select_related('product'))
    @property
    def discount(self): return self.subtotal*self.coupon.percent//100 if self.coupon else 0
    @property
    def total(self): return self.subtotal-self.discount
class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items'); product=models.ForeignKey(Product,on_delete=models.CASCADE); variant=models.ForeignKey(Variant,null=True,blank=True,on_delete=models.SET_NULL); quantity=models.PositiveIntegerField(default=1)
    class Meta: unique_together=[('cart','product','variant')]
    @property
    def total(self): return self.quantity*(self.product.price+(self.variant.extra_price if self.variant else 0))
class Address(TimeStamped):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='addresses'); title=models.CharField(max_length=60,default='آدرس اصلی'); receiver=models.CharField(max_length=100); phone=models.CharField(max_length=20); province=models.CharField(max_length=60); city=models.CharField(max_length=60); postal_code=models.CharField(max_length=15); address=models.TextField(); is_default=models.BooleanField(default=False)
    class Meta: verbose_name='آدرس'; verbose_name_plural='آدرس‌ها'
class Order(TimeStamped):
    STATUS=[('new','جدید'),('contacted','در حال هماهنگی'),('done','نهایی شده'),('cancelled','لغو شده')]
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='orders'); code=models.CharField(max_length=12,unique=True); status=models.CharField(max_length=12,choices=STATUS,default='new'); full_name=models.CharField(max_length=120); phone=models.CharField(max_length=20); address=models.TextField(); total=models.PositiveIntegerField(); note=models.TextField(blank=True)
    class Meta: verbose_name='سفارش'; verbose_name_plural='سفارش‌ها'; ordering=['-created_at']
    def __str__(self): return f'#{self.code}'
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items'); product_title=models.CharField(max_length=180); price=models.PositiveIntegerField(); quantity=models.PositiveIntegerField(); variant_name=models.CharField(max_length=80,blank=True)
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='wishlist'); product=models.ForeignKey(Product,on_delete=models.CASCADE)
    class Meta: unique_together=[('user','product')]; verbose_name='علاقه‌مندی'; verbose_name_plural='علاقه‌مندی‌ها'
class StoreSettings(models.Model):
    telegram_id=models.CharField(max_length=80,default='@YOUR_TELEGRAM_ID'); announcement=models.CharField(max_length=180,blank=True,default='ارسال رایگان برای سفارش‌های بالای ۲ میلیون تومان ✦')
    class Meta: verbose_name='تنظیمات فروشگاه'; verbose_name_plural='تنظیمات فروشگاه'
    def __str__(self): return 'تنظیمات عمومی'
