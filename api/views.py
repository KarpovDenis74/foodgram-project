from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import IngredientSerializer
from recipes.models import Favorite, Ingredient, Recipe, ShopList, Subscription

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
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @login_required
    @api_view(('POST', 'DELETE'))
    @renderer_classes((JSONRenderer,))
    def set_subscriptions(request, author_id):
        author = get_object_or_404(User, pk=author_id)
        context = {'context': 'OK'}
        if request.user == author:
            context = {'context': 'False'}
            return Response(context, status=status.HTTP_200_OK)
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
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        context = {'context': 'OK'}
        if request.method == 'POST':
            favorite = Favorite(user=request.user,
                                recipe=recipe)
            favorite.save()
            return Response(context, status=status.HTTP_200_OK)
        favorite = get_object_or_404(Favorite,
                                     user=request.user,
                                     recipe=recipe)
        favorite.delete()
        return Response(context, status=status.HTTP_200_OK)

    @api_view(('POST', 'DELETE'))
    @renderer_classes((JSONRenderer,))
    def set_purchases(request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if not request.user.is_authenticated:
            context = {'success': True}
            if request.method == 'POST':
                Api._guest_post_set_purchases(request, recipe_id)
                return Response(context, status=status.HTTP_200_OK)
            if request.session.get('purchases'):
                if recipe_id in request.session.get('purchases'):
                    request.session['purchases'].remove(recipe_id)
                    request.session.save()
            return Response(context, status=status.HTTP_200_OK)
        if request.method == 'POST':
            try:
                shop_list = ShopList(user=request.user, recipe=recipe)
                shop_list.save()
                context = {'success': True}
                return Response(context, status=status.HTTP_200_OK)
            except Exception:
                context = {'success': False}
                return Response(context, status=status.HTTP_200_OK)
        try:
            shop_list = ShopList.objects.get(user=request.user, recipe=recipe)
            shop_list.delete()
            context = {'success': True}
            return Response(context, status=status.HTTP_200_OK)
        except Exception:
            context = {'success': False}
            return Response(context, status=status.HTTP_200_OK)

    def _guest_post_set_purchases(request, recipe_id):
        if request.session.get('purchases'):
            if recipe_id not in (request.session['purchases']):
                request.session['purchases'].append(recipe_id)
                request.session.save()
        else:
            request.session['purchases'] = [recipe_id, ]
            request.session.save()
