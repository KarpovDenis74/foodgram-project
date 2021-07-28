from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from recipes.models import (Favorite, Ingredient, Subscription,
                            Recipe)
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serialisers import (IngredientSerializer,
                             )
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer

User = get_user_model()


class Api(APIView):
    @api_view(('GET',))
    @renderer_classes((JSONRenderer,))
    def get_ingredients(request):
        param = str(request.GET.get('query', None))
        if param is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ingredient = Ingredient.objects.filter(title__icontains=param)
        serialiser = IngredientSerializer(ingredient, many=True)
        if serialiser.is_valid:
            return Response(serialiser.data, status=status.HTTP_200_OK)
        return Response(status=status.TTP_400_BAD_REQUEST)

    @login_required
    @api_view(('POST', 'DELETE'))
    @renderer_classes((JSONRenderer,))
    def set_subscriptions(request, author_id):
        author = get_object_or_404(User, pk=author_id)
        context = {'context': 'OK'}
        if request.method == 'POST':
            try:
                subscription = Subscription(user=request.user,
                                            author=author)
                subscription.save()
            except Exception:
                context = {'context': 'False'}
            return Response(context, status=status.HTTP_200_OK)
        try:
            subscription = Subscription.objects.get(
                user=request.user, author=author)
            subscription.delete()
        except Exception:
            pass
        return Response(context, status=status.HTTP_200_OK)

    @login_required
    @api_view(('POST', 'DELETE'))
    @renderer_classes((JSONRenderer,))
    def set_favorites(request, recipe_id):
        print(request)
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        context = {'context': 'OK'}
        if request.method == 'POST':
            try:
                favorite = Favorite(user=request.user,
                                    recipe=recipe)
                favorite.save()
            except Exception:
                pass
            return Response(context, status=status.HTTP_200_OK)
        try:
            favorite = Favorite.objects.get(user=request.user, recipe=recipe)
            favorite.delete()
        except Exception:
            pass
        return Response(context, status=status.HTTP_200_OK)
