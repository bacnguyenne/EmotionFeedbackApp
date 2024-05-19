from django.contrib import admin
from .models import Address, Category, Product, Cart, Order, EmotionData

class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'locality', 'city', 'state')
    list_filter = ('city', 'state')
    list_per_page = 10
    search_fields = ('locality', 'city', 'state')
    actions = ['delete_selected']

    def has_delete_permission(self, request, obj=None):
        return True

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category_image', 'is_active', 'is_featured', 'updated_at')
    list_editable = ('slug', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured')
    list_per_page = 10
    search_fields = ('title', 'description')
    prepopulated_fields = {"slug": ("title", )}
    actions = ['delete_selected']

    def has_delete_permission(self, request, obj=None):
        return True

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'product_image', 'is_active', 'is_featured', 'updated_at')
    list_editable = ('slug', 'category', 'is_active', 'is_featured')
    list_filter = ('category', 'is_active', 'is_featured')
    list_per_page = 10
    search_fields = ('title', 'category__title', 'short_description')
    prepopulated_fields = {"slug": ("title", )}
    actions = ['delete_selected']

    def has_delete_permission(self, request, obj=None):
        return True

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_at')
    list_editable = ('quantity',)
    list_filter = ('created_at',)
    list_per_page = 20
    search_fields = ('user__username', 'product__title')
    actions = ['delete_selected']

    def has_delete_permission(self, request, obj=None):
        return True

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'status', 'ordered_date')
    list_editable = ('quantity', 'status')
    list_filter = ('status', 'ordered_date')
    list_per_page = 20
    search_fields = ('user__username', 'product__title')
    actions = ['delete_selected']

    def has_delete_permission(self, request, obj=None):
        return True

@admin.register(EmotionData)
class EmotionDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'joy', 'sadness', 'surprise', 'anger', 'fear', 'disgust', 'timestamp')
    search_fields = ('user__username', 'timestamp')
    list_filter = ('user', 'timestamp') 

admin.site.register(Address, AddressAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
