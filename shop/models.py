# from decimal import Decimal
# from django.db import models
# from .abstract_model import TimestampedModel
#
#
# class Category(models.Model):
#     name = models.CharField(
#         max_length=100, verbose_name='Category name'
#     )
#     slug = models.SlugField(
#         max_length=70, unique=True
#     )
#
#     class Meta:
#         verbose_name_plural = 'Categories'
#
#     def __str__(self):
#         return self.name
#
#
# class Image(models.Model):
#     product = models.ForeignKey(
#         'shop.Product',
#         on_delete=models.CASCADE,
#         related_name='images',
#     )
#     image = models.ImageField(
#         upload_to='images/product', max_length=300
#     )
#     url = models.URLField(
#         max_length=512, verbose_name='Image URL'
#     )
#     size = models.PositiveIntegerField(
#         blank=True, null=True
#     )
#
#     def __str__(self):
#         return self.image.url
#
#
# class Product(TimestampedModel):
#     source_url = models.URLField(
#         verbose_name='Source URL', max_length=500
#     )
#     title = models.CharField(
#         max_length=200
#     )
#     slug = models.SlugField(
#         max_length=150, unique=True
#     )
#     description = models.TextField(
#         blank=True, default=''
#     )
#     characteristics = models.TextField(
#         blank=True, default=''
#     )
#     price = models.DecimalField(
#         max_digits=10, decimal_places=2,
#         blank=True, null=True
#     )
#     old_price = models.DecimalField(
#         max_digits=10, decimal_places=2,
#         blank=True, null=True, verbose_name='Old Price'
#     )
#     article = models.CharField(
#         max_length=30
#     )
#     categories = models.ManyToManyRel(
#         Category,
#         related_name='product'
#     )
#
#     def save(self, *args, **kwargs) -> None:
#         if self.old_price:
#             self.discount = Decimal(
#                 round((float(self.price) / float(self.old_price))
#                       * 100 - 100, 2)
#             )
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return self.title