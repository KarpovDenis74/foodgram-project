import io

from django.conf import settings
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from recipes.models import Favorite, MealTime, ShopList, Subscription


def get_actual_tags(request_get):
    seted_tags = request_get.getlist('tags')
    all_tags = list(MealTime.objects.all())
    tags = []
    seted_tags_pk = []
    all_tags_pk = []
    all_tags_seted = []
    all_tags_is_null = True
    for tag in all_tags:
        if tag.name_english in seted_tags:
            tags.append({'enabled': True,
                         'name': tag.name_english})
            seted_tags_pk.append(tag.pk)
            all_tags_is_null = False
        else:
            tags.append({'enabled': False,
                         'name': tag.name_english})
            all_tags_pk.append(tag.pk)
            all_tags_seted.append({'enabled': True,
                                   'name': tag.name_english})
    if all_tags_is_null:
        seted_tags_pk = all_tags_pk
        tags = all_tags_seted
    return seted_tags_pk, tags


def get_recipes_full(request, recipes):
    recipes_full = []
    for recipe in recipes:
        favorite = ''
        _tags = []
        if request.user.is_authenticated:
            favorite = list(Favorite.objects.filter(recipe=recipe,
                                                    user=request.user))
            shop_list = ShopList.objects.filter(user=request.user,
                                                recipe=recipe)
        else:
            favorite = False
            shop_list = recipe.pk in request.session.get('purchases', ())
        seted_tags = list(MealTime.objects.filter(rmt_mt__recipes=recipe))
        all_tags = list(MealTime.objects.all())
        for tag in all_tags:
            if tag in seted_tags:
                _tags.append({'name_en': tag.name_english,
                              'name_ru': tag.name_russian,
                              'enabled': True})
            else:
                _tags.append({'name_en': tag.name_english,
                              'name_ru': tag.name_russian,
                              'enabled': False})
        recipes_full.append([recipe, favorite, _tags, shop_list])
    return recipes_full


def get_pdf(ingredients):
    pdfmetrics.registerFont(TTFont(
        'FreeSans',
        settings.STATIC_ROOT + '/Font/FreeSans.ttf'))
    buffer = io.BytesIO()
    page = canvas.Canvas(buffer)
    page.setFont("FreeSans", 20)
    page.setFillColorRGB(0.6, 0.3, 0.6)
    page.drawString(200, 780, "Продуктовый помощник")
    page.line(100, 750, 495, 750)
    text_object = page.beginText(150, 700)
    text_object.setFont("FreeSans", 14)
    for ingredient in ingredients:
        text_object.textLine(f'{ingredient.title}: '
                             f'{ingredient.count} '
                             f' {ingredient.dimension}')
    page.drawText(text_object)
    page.line(0, 841, 595, 841)
    page.line(100, 100, 495, 100)
    page.setFont("FreeSans", 10)
    page.drawString(250, 50, "Приятного аппетита !!!")
    page.showPage()
    page.save()
    buffer.seek(0)
    return buffer


def get_shop_list_count(request):
    if request.user.is_authenticated:
        shop_list_count = (ShopList
                           .objects
                           .filter(user=request.user).count())
    elif request.session.get('purchases'):
        shop_list_count = len(request.session['purchases'])
        print(f'shop_list_count = {shop_list_count}')
    else:
        shop_list_count = 0
        print(f'shop_list_count = {shop_list_count}')
    return shop_list_count


def get_subscription(request, author):
    try:
        subscription = Subscription.objects.get(user=request.user,
                                                author=author)
    except Exception:
        subscription = False
    return subscription


def get_favorite(request, recipe):
    try:
        favorite = Favorite.objects.get(user=request.user, recipe=recipe)
    except Exception:
        favorite = False
    return favorite


def get_shop_list(request, recipe):
    if request.user.is_authenticated:
        try:
            shop_list = ShopList.objects.get(user=request.user, recipe=recipe)
        except Exception:
            shop_list = False
        return shop_list
    elif request.session.get('purchases'):
        shop_list = recipe.pk in request.session.get('purchases')
        print(f'shop_list = {shop_list}')
    else:
        shop_list = False
        print(f'shop_list = {shop_list}')
    return shop_list
