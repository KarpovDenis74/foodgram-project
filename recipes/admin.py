from django.contrib import admin

from recipes.models import (Favorite, Ingredient, MealTime, Recipe,
                            RecipeIngredient, RecipeMealTime, ShopList,
                            Subscription)


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
    list_filter = ("dimension", "title", )
    empty_value_display = "-пусто-"


class RecipeAdmin(admin.ModelAdmin):
    inlines = [MembershipInline, MembershipInline1]
    search_fields = ("name",)
    list_filter = ("time_cooking", "name", )
    empty_value_display = "-пусто-"


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "recipes", "ingredient", "amount")
    search_fields = ("recipes", "ingredient")
    list_filter = ("amount",)
    empty_value_display = "-пусто-"


class RecipeMealTimeAdmin(admin.ModelAdmin):
    list_display = ("pk", "recipes", "meal_time")
    search_fields = ("recipes", "meal_time")
    list_filter = ("meal_time",)
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


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "author")
    search_fields = ("user",)
    list_filter = ("author",)
    empty_value_display = "-пусто-"


class ShopListAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "recipe")
    search_fields = ("user",)
    list_filter = ("recipe",)
    empty_value_display = "-пусто-"


admin.site.register(MealTime, MealTimeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(RecipeMealTime, RecipeMealTimeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(ShopList, ShopListAdmin)
