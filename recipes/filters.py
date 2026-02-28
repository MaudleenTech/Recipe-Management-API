import django_filters
from .models import Recipe

class RecipeFilter(django_filters.FilterSet):
    ingredient = django_filters.NumberFilter(
        field_name="recipe_ingredients__ingredient_id",
        lookup_expr="exact"
    )

    class Meta:
        model = Recipe
        fields = ["category", "ingredient"]