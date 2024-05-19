# create_products_based_on_existing.py
import os
import django
import random
from datetime import datetime
from django.utils.dateparse import parse_datetime


# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jewelryshop.settings')
django.setup()

from store.models import Product

existing_products = Product.objects.all()

# Tạo thêm 10 sản phẩm mới dựa trên dữ liệu hiện có
for i in range(1, 11):
    for product in existing_products:
        new_product = Product(
            title=f'{product.title} {i}',
            short_description=product.short_description,
            product_image=product.product_image,
            price=int(product.price * random.randint(4, 30)/10),
            is_active=product.is_active,
            is_featured=product.is_featured,
            sku=f'{product.sku}-{i}',
            category=product.category,
            slug=f'{product.slug}-{i}',
        )
        new_product.save()


