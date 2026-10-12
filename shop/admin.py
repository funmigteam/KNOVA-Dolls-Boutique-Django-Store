from django.contrib import admin
from .models import *
class GalleryInline(admin.TabularInline): model=ProductImage; extra=1
class VariantInline(admin.TabularInline): model=Variant; extra=1
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
 list_display=('title','category','price','stock','is_active','is_featured');list_filter=('category','is_active','is_featured');search_fields=('title',);prepopulated_fields={'slug':('title',)};inlines=[GalleryInline,VariantInline]
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin): list_display=('code','full_name','total','status','created_at');list_filter=('status',);search_fields=('code','full_name','phone')
admin.site.register([Category,Coupon,Cart,CartItem,Address,OrderItem,Wishlist,StoreSettings])
