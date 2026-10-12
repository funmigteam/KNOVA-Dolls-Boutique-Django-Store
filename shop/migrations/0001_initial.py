import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100, verbose_name='نام دسته')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='categories/')),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'دسته\u200cبندی',
                'verbose_name_plural': 'دسته\u200cبندی\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30, unique=True)),
                ('percent', models.PositiveSmallIntegerField()),
                ('active', models.BooleanField(default=True)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'کوپن',
                'verbose_name_plural': 'کوپن\u200cها',
            },
        ),
        migrations.CreateModel(
            name='StoreSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.CharField(default='@YOUR_TELEGRAM_ID', max_length=80)),
                ('announcement', models.CharField(blank=True, default='ارسال رایگان برای سفارش\u200cهای بالای ۲ میلیون تومان ✦', max_length=180)),
            ],
            options={
                'verbose_name': 'تنظیمات فروشگاه',
                'verbose_name_plural': 'تنظیمات فروشگاه',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(default='آدرس اصلی', max_length=60)),
                ('receiver', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('province', models.CharField(max_length=60)),
                ('city', models.CharField(max_length=60)),
                ('postal_code', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('is_default', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'آدرس',
                'verbose_name_plural': 'آدرس\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('session_key', models.CharField(blank=True, max_length=40, null=True, unique=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL)),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.coupon')),
            ],
            options={
                'verbose_name': 'سبد خرید',
                'verbose_name_plural': 'سبدهای خرید',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=12, unique=True)),
                ('status', models.CharField(choices=[('new', 'جدید'), ('contacted', 'در حال هماهنگی'), ('done', 'نهایی شده'), ('cancelled', 'لغو شده')], default='new', max_length=12)),
                ('full_name', models.CharField(max_length=120)),
                ('phone', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('total', models.PositiveIntegerField()),
                ('note', models.TextField(blank=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'سفارش',
                'verbose_name_plural': 'سفارش\u200cها',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_title', models.CharField(max_length=180)),
                ('price', models.PositiveIntegerField()),
                ('quantity', models.PositiveIntegerField()),
                ('variant_name', models.CharField(blank=True, max_length=80)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='shop.order')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=180)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('short_description', models.CharField(blank=True, max_length=220)),
                ('description', models.TextField(blank=True)),
                ('price', models.PositiveIntegerField(verbose_name='قیمت (تومان)')),
                ('compare_at_price', models.PositiveIntegerField(blank=True, null=True, verbose_name='قیمت قبل')),
                ('stock', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=False, verbose_name='پیشنهاد ویژه')),
                ('is_new', models.BooleanField(default=True, verbose_name='محصول جدید')),
                ('image', models.ImageField(blank=True, upload_to='products/')),
                ('attributes', models.JSONField(blank=True, default=dict)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='shop.category', verbose_name='دسته\u200cبندی')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/gallery/')),
                ('alt', models.CharField(blank=True, max_length=120)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery', to='shop.product')),
            ],
            options={
                'verbose_name': 'تصویر محصول',
                'verbose_name_plural': 'گالری محصول',
            },
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('color', models.CharField(blank=True, max_length=40)),
                ('size', models.CharField(blank=True, max_length=30)),
                ('stock', models.PositiveIntegerField(default=0)),
                ('extra_price', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='shop.product')),
            ],
            options={
                'verbose_name': 'تنوع',
                'verbose_name_plural': 'رنگ و سایز',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='shop.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
                ('variant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.variant')),
            ],
            options={
                'unique_together': {('cart', 'product', 'variant')},
            },
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'علاقه\u200cمندی',
                'verbose_name_plural': 'علاقه\u200cمندی\u200cها',
                'unique_together': {('user', 'product')},
            },
        ),
    ]
