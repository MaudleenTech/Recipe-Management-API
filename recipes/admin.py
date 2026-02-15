from django.contrib import admin
from .models import Category, Ingredient, Recipe, RecipeIngredient


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "category", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("title", "user__username")


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ("id", "recipe", "ingredient", "quantity", "unit")
    list_filter = ("ingredient",)
    search_fields = ("recipe__title", "ingredient__name")
