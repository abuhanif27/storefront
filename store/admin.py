from django.contrib import admin,messages
from django.db.models import Count
from django.utils.html import format_html,urlencode
from django.urls import reverse
from . import models
# Register your models here.

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    LOW = "<10"
    MEDIUM = "<20"
    HIGH = ">=20"
    def queryset(self, request, queryset):
        if self.value() == self.LOW:
            return queryset.filter(inventory__lt=10)
        elif self.value() == self.MEDIUM:
            return queryset.filter(inventory__lt=20, inventory__gte=10)
        elif self.value() == self.HIGH:
            return queryset.filter(inventory__gte=20)

    def lookups(self, request, model_admin):
        return [
            (self.LOW, 'Low')
            , (self.MEDIUM, 'Medium')
            , (self.HIGH, 'High')
        ]



@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']
    list_per_page = 10
    search_fields = ['title']
    
    @admin.display(ordering='product_count')
    def product_count(self, collection):
        url = reverse('admin:store_product_changelist') + '?' + urlencode({'collection__id': str(collection.id)})
        return format_html('<a href="{}">{}</a>', url,collection.product_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count=Count('product')
        )


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {'slug': ['title']}
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory','inventory_status','collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    list_filter = ['collection','last_update',InventoryFilter]
    search_fields = ['title']

    @admin.display(ordering='collection__title')
    def collection_title(self, product):
        url = reverse('admin:store_collection_changelist') + '?' + urlencode({'id': str(product.collection.id)})
        return format_html('<a href="{}">{}</a>', url, product.collection.title)

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(request, f'{updated_count} products were successfully updated.', messages.ERROR) 

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership','orders_count']
    list_editable = ['membership']
    list_select_related = ['user']
    autocomplete_fields = ['user']
    list_per_page = 10
    search_fields = ['user__first_name__istartswith', 'user__last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = reverse('admin:store_order_changelist') + '?' + urlencode({'customer__id': str(customer.id)})
        return format_html('<a href="{}">{}</a>', url,customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )

class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    extra = 0
    min_num = 1
    max_num = 10

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    autocomplete_fields = ['customer']
    list_display = ['id', 'customer_name', 'placed_at', 'payment_status']
    list_select_related = ['customer','customer__user']
    list_per_page = 10
    list_editable = ['payment_status']

    @admin.display(ordering='customer__user__first_name')
    def customer_name(self, order):
        url = reverse('admin:store_customer_changelist') + '?' + urlencode({'id': str(order.customer.id)})
        return format_html('<a href="{}">{}</a>', url, order.customer.user.first_name + ' ' + order.customer.user.last_name)