from django.contrib import admin
from .models import AddUser,Product,Order,CartItem,Category,Cart,OrderItem
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'available', 'is_featured', 'created', 'updated')
    list_editable = ('price', 'stock', 'available', 'is_featured')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)
admin.site.register(AddUser)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(Category)
