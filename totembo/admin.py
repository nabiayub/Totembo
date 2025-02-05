from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe

admin.site.register(Reviews)
admin.site.register(Favourites)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(OrderProducts)
admin.site.register(Region)
admin.site.register(Customer)
admin.site.register(ShippingAddress)
admin.site.register(SaveOrder)
admin.site.register(SaveOrderProduct)



class ImageInlane(admin.TabularInline):
    fk_name = 'product'
    model = ProductImage
    extra = 1



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'get_photo')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',)}


    def get_photo(self, obj):
        if obj.image:
            try:
                return mark_safe(f'<img src="{obj.image.url}" width="50px" >')
            except:
                return '-'
        else:
            return '-'

    get_photo.short_description = 'Фото'



@admin.register(Brand)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',)}



@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')
    list_display_links = ('id', 'title')

    prepopulated_fields = {'slug': ('title',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'category', 'brand', 'gender', 'weight', 'quantity', 'color_name',
                    'material_korpus', 'material_bracelet', 'size', 'get_photo')
    list_display_links = ('id', 'title')
    list_filter = ('brand', 'category', 'gender', 'style')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ImageInlane]


    def get_photo(self, obj):
        try:
            if obj.product_images:
                return mark_safe(f'<img src="{obj.product_images.first().image.url}" width="50">')

            else:
                return '-'
        except:
            return '-'

    get_photo.short_description = 'Фото'






