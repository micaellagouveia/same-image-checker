from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from images_checker import models


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'cnpj',
    ]

    search_fields = [
        'name',
        'cnpj',
    ]


@admin.register(models.Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'address',
    ]

    search_fields = [
        'address',
    ]


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    exclude = [
        'image_hash',
    ]

    list_display = [
        'id',
        'url',
        'image_hash',
    ]

    search_fields = [
        'id',
        'url',
        'image_hash',
    ]