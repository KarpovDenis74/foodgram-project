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
        recipe_add_property = {}
        tags_add_property = {}

        favorites = list(Favorite.objects.filter(recipe=recipe,
                                                 user=requests.user))
        for favorite in favorites:
            print(f'favorite = {favorite}')
        if len(favorites) > 0:
            recipe_add_property['favorite'] = bool(True)
        else:
            recipe_add_property['favorite'] = False
        tags = MealTime.objects.filter(rmt=recipe)
        if tags is not None:
            tags_add_property['tags'] = []
            for tag in tags:
                tags_add_property['tags'].append(tag.name_english)
        else:
            tags_add_property['tags'].append('')
        recipes_full.append([recipe, recipe_add_property, tags_add_property])
        for recipe in recipes_full:
            print(f'recipes_full = {recipe}')
    return recipes_full
