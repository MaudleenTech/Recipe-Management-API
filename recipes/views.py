from rest_framework import viewsets, permissions, filters
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from .models import Recipe, Category, Ingredient
from .serializers import RecipeSerializer, CategorySerializer, IngredientSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import RecipeFilter

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by("-created_at")
    serializer_class = RecipeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = RecipeFilter
    search_fields = [
        "title",
        "description",
        "instructions",
        "category__name",
        "recipe_ingredients__ingredient__name",
    ]
    ordering_fields = ["created_at", "prep_time", "cook_time", "servings", "title"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)