import random,string
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404,redirect,render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from .forms import AddressForm,CheckoutForm,RegisterForm
from .models import *

def get_cart(request):
    if request.user.is_authenticated: return Cart.objects.get_or_create(user=request.user)[0]
    if not request.session.session_key: request.session.create()
    return Cart.objects.get_or_create(session_key=request.session.session_key)[0]
def home(request):
    return render(request,'shop/home.html',{'categories':Category.objects.filter(active=True)[:6],'new_products':Product.objects.filter(is_active=True,is_new=True)[:8],'featured':Product.objects.filter(is_active=True,is_featured=True)[:4],'deals':Product.objects.filter(is_active=True,compare_at_price__isnull=False)[:4]})
def products(request):
    qs=Product.objects.filter(is_active=True).select_related('category'); q=request.GET.get('q',''); cat=request.GET.get('category',''); sort=request.GET.get('sort','new')
    if q: qs=qs.filter(Q(title__icontains=q)|Q(description__icontains=q))
    if cat: qs=qs.filter(category__slug=cat)
    qs=qs.order_by('price' if sort=='cheap' else '-price' if sort=='expensive' else '-created_at')
    return render(request,'shop/products.html',{'products':qs,'categories':Category.objects.filter(active=True),'query':q,'selected':cat})
def category_detail(request,slug):
    category=get_object_or_404(Category,slug=slug,active=True)
    return render(request,'shop/category_detail.html',{'category':category,'products':category.products.filter(is_active=True),'categories':Category.objects.filter(active=True)})
def collections(request):
    collections=[
      {'title':'دوستان جنگل','slug':'عروسکهای-پولیشی','tone':'forest','copy':'خرس‌ها، خرگوش‌ها و همراه‌های گرمِ جنگل.'},
      {'title':'شب پرستاره','slug':'عروسکهای-کلکسیونی','tone':'night','copy':'شخصیت‌هایی کوچک برای رؤیاهای بزرگ.'},
      {'title':'دنیای پاستلی','slug':'مینیفیگور','tone':'pastel','copy':'مینی‌فیگورهای رنگی برای ساختن قصه.'},
      {'title':'جزئیات دوست‌داشتنی','slug':'اکسسوری-عروسک','tone':'accessory','copy':'لباس و اکسسوری برای کامل شدن هر دوست.'},
    ]
    return render(request,'shop/collections.html',{'collections':collections})
def product_detail(request,slug):
    p=get_object_or_404(Product,slug=slug,is_active=True)
    return render(request,'shop/product_detail.html',{'product':p,'related':Product.objects.filter(category=p.category,is_active=True).exclude(pk=p.pk)[:4]})
def add_cart(request,product_id):
    p=get_object_or_404(Product,pk=product_id,is_active=True); cart=get_cart(request); qty=max(1,int(request.POST.get('quantity',1))); variant=p.variants.filter(pk=request.POST.get('variant')).first() if request.POST.get('variant') else None; available=variant.stock if variant else p.stock
    item,_=CartItem.objects.get_or_create(cart=cart,product=p,variant=variant,defaults={'quantity':0}); item.quantity=min(item.quantity+qty,available); item.save()
    if request.headers.get('x-requested-with')=='XMLHttpRequest': return JsonResponse({'ok':True,'count':sum(x.quantity for x in cart.items.all()),'message':'به سبد خرید اضافه شد'})
    messages.success(request,'محصول به سبد خرید اضافه شد.'); return redirect(request.META.get('HTTP_REFERER','shop:cart'))
def cart(request): return render(request,'shop/cart.html',{'cart':get_cart(request)})
def update_cart(request,item_id):
    item=get_object_or_404(CartItem,pk=item_id,cart=get_cart(request))
    if request.POST.get('action')=='remove': item.delete()
    else: item.quantity=max(1,min(int(request.POST.get('quantity',item.quantity)),item.variant.stock if item.variant else item.product.stock)); item.save()
    return redirect('shop:cart')
def apply_coupon(request):
    cart=get_cart(request); coupon=Coupon.objects.filter(code=request.POST.get('code','').upper(),active=True).first()
    if coupon: cart.coupon=coupon;cart.save();messages.success(request,'کد تخفیف اعمال شد.')
    else: messages.error(request,'کد تخفیف معتبر نیست.')
    return redirect('shop:cart')
def checkout(request):
    cart=get_cart(request)
    if not cart.items.exists(): messages.info(request,'سبد خرید شما خالی است.'); return redirect('shop:products')
    form=CheckoutForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
      with transaction.atomic():
        for i in cart.items.select_related('product','variant'):
          if i.quantity>(i.variant.stock if i.variant else i.product.stock): messages.error(request,f'موجودی «{i.product.title}» کافی نیست.'); return redirect('shop:cart')
        order=Order.objects.create(user=request.user if request.user.is_authenticated else None,code='KN'+''.join(random.choices(string.digits,k=8)),total=cart.total,**form.cleaned_data)
        for i in cart.items.select_related('product','variant'):
          OrderItem.objects.create(order=order,product_title=i.product.title,price=i.product.price,quantity=i.quantity,variant_name=i.variant.name if i.variant else '')
          i.product.stock-=i.quantity;i.product.save()
          if i.variant: i.variant.stock-=i.quantity;i.variant.save()
        cart.items.all().delete()
      settings=StoreSettings.objects.first();return render(request,'shop/order_success.html',{'order':order,'telegram':settings.telegram_id if settings else '@YOUR_TELEGRAM_ID'})
    return render(request,'shop/checkout.html',{'cart':cart,'form':form})
def register(request):
    form=RegisterForm(request.POST or None)
    if request.method=='POST' and form.is_valid(): login(request,form.save());messages.success(request,'به خانواده KNOVA خوش آمدید.');return redirect('shop:home')
    return render(request,'registration/register.html',{'form':form})
@login_required
def dashboard(request): return render(request,'shop/dashboard.html',{'orders':request.user.orders.all(),'addresses':request.user.addresses.all(),'form':AddressForm()})
@login_required
def add_address(request):
    form=AddressForm(request.POST)
    if form.is_valid(): a=form.save(commit=False);a.user=request.user;a.save();messages.success(request,'آدرس ذخیره شد.')
    return redirect('shop:dashboard')
@login_required
def wishlist(request,product_id):
    p=get_object_or_404(Product,pk=product_id);obj,created=Wishlist.objects.get_or_create(user=request.user,product=p)
    if not created: obj.delete();messages.info(request,'از علاقه‌مندی‌ها حذف شد.')
    else: messages.success(request,'به علاقه‌مندی‌ها افزوده شد.')
    return redirect(request.META.get('HTTP_REFERER','shop:home'))
@staff_member_required
def admin_dashboard(request):
    orders=Order.objects.exclude(status='cancelled')
    return render(request,'shop/admin_dashboard.html',{'sales':orders.aggregate(total=Sum('total'))['total'] or 0,'order_count':orders.count(),'low_stock':Product.objects.filter(stock__lte=3),'best_sellers':OrderItem.objects.values('product_title').annotate(qty=Sum('quantity')).order_by('-qty')[:5],'recent_orders':Order.objects.all()[:6]})
def about(request): return render(request,'shop/about.html')
def contact(request): return render(request,'shop/contact.html')
def faq(request): return render(request,'shop/faq.html')
def rules(request): return render(request,'shop/rules.html')
