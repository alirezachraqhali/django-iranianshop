from django.db import models

# Create your models here.
class Product(models.Model):
    def upload_photo(instance, file_name:str):
        import datetime
        n = datetime.datetime.now().__str__().replace('_', '-').replace(' ', '_').replace(':', '-')
        ext = file_name.split('.')[-1]
        return f'images/product/{n}.{ext}'
    name = models.CharField('عنوان محصول', max_length=255, null=False, blank=False)
    price = models.DecimalField('قیمت', decimal_places=0, max_digits=12, null=False, blank=False)
    total = models.IntegerField('تعداد', default=5, null=False, blank=False)
    photo = models.ImageField('تصویر', upload_to=upload_photo, null=False, blank=False)
    description = models.TextField('توضیحات تکمیلی', null=True, blank=True)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.name
    