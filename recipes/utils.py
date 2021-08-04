from recipes.models import Favorite, MealTime


def get_actual_tags(request_get):
    seted_tags = request_get.getlist('tags')
    print(f'seted_tags = {seted_tags}')
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


def get_recipes_full(requests, recipes):
    recipes_full = []
    for recipe in recipes:
        favorite = ''
        _tags = []
        favorites = list(Favorite.objects.filter(recipe=recipe,
                                                 user=requests.user))
        if len(favorites) > 0:
            favorite = 'on'
        else:
            favorite = 'off'
        seted_tags = list(MealTime.objects.filter(rmt=recipe))
        all_tags = list(MealTime.objects.all())
        if seted_tags is not None:
            for tag in all_tags:
                if tag in seted_tags:
                    _tags.append({'name_en': tag.name_english,
                                  'name_ru': tag.name_russian,
                                  'enabled': True})
                else:
                    _tags.append({'name_en': tag.name_english,
                                  'name_ru': tag.name_russian,
                                  'enabled': False})

        recipes_full.append([recipe, favorite, _tags])
    return recipes_full
