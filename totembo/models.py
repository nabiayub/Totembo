from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название категории')
    slug = models.SlugField(unique=True, null=True)
    image = models.ImageField(upload_to='category_images/', null=True, verbose_name='Фото')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'


class Gender(models.Model):
    title = models.CharField(max_length=100, verbose_name='Гендер')
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Пол'


class Style(models.Model):
    title = models.CharField(max_length=100, verbose_name='Стиль')
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Стиль'
        verbose_name_plural = 'Стили'


class Brand(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название бренда')
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название продукта')
    slug = models.SlugField(unique=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    size = models.CharField(max_length=50, verbose_name='Размер')
    color_name = models.CharField(max_length=50, verbose_name='Цвет')
    color_code = models.CharField(max_length=100, verbose_name='Код цвета')
    material_korpus = models.CharField(max_length=50, null=True, blank=True, verbose_name='Материал корпуса')
    material_bracelet = models.CharField(max_length=50, null=True, blank=True, verbose_name='Материал браслета')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    discount = models.IntegerField(null=True, blank=True, default=0, verbose_name='Скидка')
    price = models.FloatField(default=0, verbose_name='Цена')
    description = models.CharField(max_length=400, verbose_name='Описание')
    style = models.ManyToManyField(Style, verbose_name='Стиль')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Бренд')
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, verbose_name='Пол')
    weight = models.FloatField(default=0, verbose_name='Вес')

    def __str__(self):
        return self.title

    def get_product_first_photo(self):
        try:
            if self.product_images:
                return self.product_images.first().photo.url
            else:
                return 'https://taplink.st/p/4/4/9/a/58792273.png?0'
        except:
            return 'https://taplink.st/p/4/4/9/a/58792273.png?0'

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт',
                                related_name='product_images')
    photo = models.ImageField(upload_to='product_images/', verbose_name='Фото')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Фото продукта'
        verbose_name_plural = 'Фото продуктов'


class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    text = models.CharField(max_length=200, verbose_name='Текст')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.BooleanField(default=False, verbose_name='Статус обновления')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                               verbose_name='Родитель')

    def __str__(self):
        return f'Продукт: {self.product.title} пользователь: {self.user.username}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Favourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')

    def __str__(self):
        return f'Продукт: {self.product.title} пользователь: {self.user.username}'

    class Meta:
        verbose_name = 'Избранный продукт'
        verbose_name_plural = 'Избранные продукты'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = models.CharField(max_length=50, verbose_name='Номер телефона')
    city = models.CharField(max_length=50, verbose_name='Город', null=True, blank=True)
    street = models.CharField(max_length=50, verbose_name='Улица', null=True, blank=True)
    home = models.CharField(max_length=50, verbose_name='Дом №:', null=True, blank=True)
    flat = models.CharField(max_length=50, verbose_name='Квартира №: ', null=True, blank=True)

    def __str__(self):
        return f'Профиль: {self.user.username}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    first_name = models.CharField(max_length=50, default='', verbose_name='Имя')
    last_name = models.CharField(max_length=50, default='', verbose_name='Фамилия')
    telegram = models.CharField(max_length=50, blank=True, null=True, verbose_name='Телеграм')

    def __str__(self):
        return f' пользователь: {self.user.username}'

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name='Покупатель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_completed = models.BooleanField(default=False, verbose_name='Статус выполнения')
    is_delivered = models.BooleanField(default=False, verbose_name='Статус доставки')

    def __str__(self):
        return f'Покупатель: {self.customer.user.username} номер заказа: {self.pk}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    @property
    def get_cart_total_price(self):
        ordered_products = self.ordered_products.all()
        total_price_of_all_products = sum([product.get_product_price_with_discount for product in ordered_products])
        return total_price_of_all_products


    @property
    def get_total_quantity_of_products(self):
        ordered_products = self.ordered_products.all()
        total_quantity_of_all_products = sum([product.quantity for product in ordered_products])
        return total_quantity_of_all_products



class OrderProducts(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name='ordered_products', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Продукт')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return f'Продукт: {self.product.title} заказ № {self.order.pk}'

    class Meta:
        verbose_name = 'Продукт заказа'
        verbose_name_plural = 'Продукты заказа'

    @property
    def get_product_price_with_discount(self):
        price = self.product.price
        if self.product.discount:
            percent = (price * self.product.discount) / 100
            price -= percent

        total_price_of_one_product = price * self.quantity
        return total_price_of_one_product




class ShippingAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Заказ')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True,  blank=True, verbose_name='Покупатель')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    phone = models.CharField(max_length=200, verbose_name='Номер телефона')
    region = models.ForeignKey('Region', on_delete=models.SET_NULL, null=True, verbose_name='Регион')
    comment = models.CharField(max_length=400, null=True, blank=True, verbose_name='Комментарий к заказу')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


    def __str__(self):
        return f'Покупатель: {self.customer.user.username} '

    class Meta:
        verbose_name = 'Адрес заказа'
        verbose_name_plural = 'Адреса заказа'


class Region(models.Model):
    region = models.CharField(max_length=100, verbose_name='Регион')

    def __str__(self):
        return self.region

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'



class SaveOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, verbose_name='Покупатель')
    order_number = models.IntegerField(verbose_name='Номер заказа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    total_price = models.FloatField(default=0, verbose_name='Сумма чека')
    completed = models.BooleanField(default=False, verbose_name='Статус заказа')

    def __str__(self):
        return f'Закза №: {self.order_number} '

    class Meta:
        verbose_name = 'Сохранённый заказ'
        verbose_name_plural = 'Сохранённые заказы'



class SaveOrderProduct(models.Model):
    order = models.ForeignKey(SaveOrder, on_delete=models.CASCADE, related_name='products', verbose_name='Заказ')
    product = models.CharField(max_length=500, verbose_name='Название товара')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    product_price = models.FloatField(verbose_name='Цена товара')
    final_price = models.FloatField(verbose_name='Сумма')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата покупки')
    photo = models.ImageField(upload_to='images/', verbose_name='Фото товара')
    color_name = models.CharField(max_length=100, verbose_name='Цвет товара')


    def __str__(self):
        return f'Товар: {self.product} заказ №: {self.order.order_number} '

    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказов'

    def get_photo(self):
        if self.photo:
            return self.photo
        else:
            return '-'






