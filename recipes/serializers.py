from rest_framework import serializers
from .models import Category, Ingredient, Recipe, RecipeIngredient


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name"]


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)
    ingredient_id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source="ingredient",
        write_only=True,
    )

    class Meta:
        model = RecipeIngredient
        fields = ["id", "ingredient", "ingredient_id", "quantity", "unit"]


class RecipeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True,
        required=False,
        allow_null=True,
    )

    # nested recipe ingredients (read + write)
    recipe_ingredients = RecipeIngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            "id",
            "user",
            "title",
            "description",
            "instructions",
            "prep_time",
            "cook_time",
            "servings",
            "category",
            "category_id",
            "recipe_ingredients",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        recipe_ingredients_data = validated_data.pop("recipe_ingredients", [])
        recipe = Recipe.objects.create(**validated_data)

        for ri in recipe_ingredients_data:
            RecipeIngredient.objects.create(recipe=recipe, **ri)

        return recipe

    def update(self, instance, validated_data):
        recipe_ingredients_data = validated_data.pop("recipe_ingredients", None)

        # update recipe fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # if recipe_ingredients provided, replace them
        if recipe_ingredients_data is not None:
            instance.recipe_ingredients.all().delete()
            for ri in recipe_ingredients_data:
                RecipeIngredient.objects.create(recipe=instance, **ri)

        return instance
            
    def validate(self, attrs):
        title = attrs.get("title") or getattr(self.instance, "title", None)
        instructions = attrs.get("instructions") or getattr(self.instance, "instructions", None)

        if not title:
            raise serializers.ValidationError({"title": "Title is required."})
        if not instructions:
            raise serializers.ValidationError({"instructions": "Instructions are required."})

        # On create, ensure at least one ingredient
        if self.instance is None:
            recipe_ingredients = self.initial_data.get("recipe_ingredients")
            if not recipe_ingredients or len(recipe_ingredients) == 0:
                raise serializers.ValidationError(
                    {"recipe_ingredients": "At least one ingredient is required."}
                )        

        return attrs