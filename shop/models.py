from django.db import models
from django.urls import reverse
from parler.models import (TranslatableModel,
                           TranslatedFields)
from django.utils.translation import gettext_lazy as _


class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Name"), max_length=200,
                              db_index=True),
        slug=models.SlugField(_("Slug"), max_length=200,
                              unique=True)
    )

    class Meta:
        # ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[str(self.slug)])

    def __str__(self):
        return self.name


class Product(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Name"), max_length=200,
                              db_index=True),
        slug=models.SlugField(_("Slug"), max_length=200,
                              db_index=True),
        description=models.TextField(_("Description"), blank=True)
    )
    category = models.ForeignKey(Category, related_name='products',
                                 on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/%Y/%m/%d',
                              blank=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # class Meta:
    #     ordering = ('name',)
    #     index_together = (('id', 'slug'),)

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[str(self.id),
                             str(self.slug)])

    def __str__(self):
        return self.name
