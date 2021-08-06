from django.contrib import admin
from recipes.models import (Ingredient, Recipe,
                            RecipeIngredient, MealTime,
                            RecipeMealTime, Favorite)


class MembershipInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 1
    extra = 0


class MembershipInline1(admin.TabularInline):
    model = RecipeMealTime
    min_num = 1
    extra = 0


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "dimension")
    search_fields = ("title",)
    list_filter = ("dimension",)
    empty_value_display = "-пусто-"


class RecipeAdmin(admin.ModelAdmin):
    inlines = [MembershipInline, MembershipInline1]
    search_fields = ("name",)
    list_filter = ("time_cooking",)
    empty_value_display = "-пусто-"


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "recipes", "ingredient", "amount")
    search_fields = ("recipes", "ingredient")
    list_filter = ("amount",)
    empty_value_display = "-пусто-"


class MealTimeAdmin(admin.ModelAdmin):
    list_display = ("pk", "name_english", "name_russian")
    search_fields = ("name_english", "name_russian")
    empty_value_display = "-пусто-"


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "recipe")
    search_fields = ("user",)
    list_filter = ("recipe",)
    empty_value_display = "-пусто-"


admin.site.register(MealTime, MealTimeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
