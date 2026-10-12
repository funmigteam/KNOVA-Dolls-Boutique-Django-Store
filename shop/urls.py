from django.contrib.auth import views as auth
from django.urls import path
from . import views
app_name = 'shop'
urlpatterns = [
 path('',views.home,name='home'), path('products/',views.products,name='products'), path('collections/',views.collections,name='collections'), path('category/<str:slug>/',views.category_detail,name='category_detail'), path('products/<str:slug>/',views.product_detail,name='product_detail'),
 path('cart/',views.cart,name='cart'), path('cart/add/<int:product_id>/',views.add_cart,name='add_cart'), path('cart/item/<int:item_id>/',views.update_cart,name='update_cart'), path('coupon/',views.apply_coupon,name='coupon'), path('checkout/',views.checkout,name='checkout'),
 path('register/',views.register,name='register'), path('login/',auth.LoginView.as_view(template_name='registration/login.html'),name='login'), path('logout/',auth.LogoutView.as_view(),name='logout'), path('password-reset/',auth.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),name='password_reset'),
 path('account/',views.dashboard,name='dashboard'), path('address/add/',views.add_address,name='add_address'), path('wishlist/<int:product_id>/',views.wishlist,name='wishlist'), path('about/',views.about,name='about'),path('contact/',views.contact,name='contact'),path('faq/',views.faq,name='faq'),path('rules/',views.rules,name='rules'),path('staff/overview/',views.admin_dashboard,name='admin_dashboard')]
