import django_filters
from .models import Recipe

class RecipeFilter(django_filters.FilterSet):
    # filter by ingredient id: /api/recipes/?ingredient=3
    ingredient = django_filters.NumberFilter(field_name="recipe_ingredients__ingredient_id")

    # optional: filter by multiple ingredient ids: /api/recipes/?ingredients=1,3,5
    ingredients = django_filters.CharFilter(method="filter_ingredients")

    def filter_ingredients(self, queryset, name, value):
        ids = [v.strip() for v in value.split(",") if v.strip().isdigit()]
        if not ids:
            return queryset
        for ing_id in ids:
            queryset = queryset.filter(recipe_ingredients__ingredient_id=int(ing_id))
        return queryset.distinct()

    class Meta:
        model = Recipe
        fields = ["category", "prep_time", "cook_time", "servings", "ingredient", "ingredients"]