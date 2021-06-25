from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from . import models


@register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'dimension',
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'title',
        'dimension',
    )


class RecipeIngredientInline(admin.TabularInline):
    model = models.RecipeIngredient
    min_num = 1
    extra = 0


@register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'publication_date',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'author',
        'name',
    )
    autocomplete_fields = (
        'ingredients',
    )
    inlines = (
        RecipeIngredientInline,
    )


@register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    fields = (
        'user',
        'recipe',
    )
    search_fields = (
        'user',
        'recipe',
    )


@register(models.Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author',
    )
    search_fields = (
        'user',
    )
    list_filter = (
        'author',
    )


@register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'name',
    )


class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff'

    )
    list_filter = (
        'email',
        'first_name'
    )


admin.site.unregister(models.User)
admin.site.register(models.User, CustomUserAdmin)
