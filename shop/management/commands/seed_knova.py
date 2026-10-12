from django.core.management.base import BaseCommand
from shop.models import Category,Product,StoreSettings,Coupon
class Command(BaseCommand):
 help='ساخت داده‌های نمونه KNOVA'
 def handle(self,*args,**kwargs):
  StoreSettings.objects.get_or_create(pk=1)
  Product.objects.all().delete()
  Category.objects.all().delete()
  data={'عروسک‌های کلکسیونی':['موس KNOVA','لیلیِ ستاره‌ای','آوا و خرگوشش','نورا، دوست جنگل'],'عروسک‌های پولیشی':['خرس کاراملی','خرگوش ابری','گربه‌ی وانیلی','اردک لیمویی'],'مینی‌فیگور':['مینی مایا','مینی نوا','مینی رها','مینی ستاره'],'اکسسوری عروسک':['کوله‌ی کوچک','لباس سیج','تاج گل لیلی','پتو ابر نرم']}
  assets=['doll-lulu.png','doll-bamboo.png','doll-milo.png']
  personas=[('لولو','خیال‌باف و مهربان','سیج'),('بامبو','ماجراجوی کوچک','کاراملی'),('میلو','آرام و شب‌دوست','یاسی')]
  for ci,(cat,names) in enumerate(data.items()):
   c=Category.objects.create(title=cat,description='یک شخصیت دوست‌داشتنی برای کلکسیون شما')
   for i,name in enumerate(names):
    person=personas[(ci+i)%3]
    Product.objects.create(title=name,category=c,price=380000+(ci*85000)+(i*45000),compare_at_price=(450000+(ci*90000)+(i*50000)) if i%2==0 else None,stock=8+i,image='products/'+assets[(ci+i)%3],short_description=f'«{person[0]}»؛ یک عروسک خاص و پرشخصیت برای همراهی با روزهای شما.',description=f'داستان {person[0]}: {person[1]}. با جزئیات ظریف، دوخت باکیفیت و طراحی منحصربه‌فرد KNOVA؛ مناسب هدیه و کلکسیون.',is_featured=i==0,attributes={'جنس':'پارچه‌ی نرم و پولیشی','ارتفاع':'۳۲ سانتی‌متر','رنگ موردعلاقه':person[2],'شخصیت':person[1],'رده سنی':'۳ سال به بالا'})
  Coupon.objects.get_or_create(code='KNOVA10',defaults={'percent':10})
  self.stdout.write(self.style.SUCCESS('داده‌های نمونه KNOVA ساخته شد.'))
