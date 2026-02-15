from django.conf import settings
from django.db import models


class Category(models.Model):
    """
    Category model.
    Stores recipe categories (e.g., Breakfast, Lunch, Dinner, Snacks).
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Ingredient model.
    Stores ingredients that can be linked to recipes (e.g., Rice, Tomato, Salt).
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Recipe model.
    Stores recipe information and links each recipe to:
    - a user (creator/owner)
    - a category
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipes"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recipes"
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    instructions = models.TextField()

    prep_time = models.PositiveIntegerField(null=True, blank=True)
    cook_time = models.PositiveIntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    """
    RecipeIngredient model (junction table).
    Handles the many-to-many relationship between Recipe and Ingredient.
    Also stores extra fields like quantity and unit.
    """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipe_ingredients"
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredient_recipes"
    )

    quantity = models.CharField(max_length=50, blank=True)
    unit = models.CharField(max_length=50, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_recipe_ingredient"
            )
        ]

    def __str__(self):
        return f"{self.ingredient.name} in {self.recipe.title}"
