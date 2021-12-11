from django.db import models


class ProducCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('-id',)


class Product(models.Model):
    category = models.ForeignKey(ProducCategory, on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=128, verbose_name='Название')
    image = models.ImageField(upload_to='products', blank=True, verbose_name='Картинка')
    short_desc = models.CharField(max_length=255, verbose_name='Краткое описание')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0, verbose_name='Цена')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    is_active = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    def delete(self):
        if self.is_active:
            self.is_active = False
        else:
            self.is_active = True
        self.save()

