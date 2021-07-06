from django.contrib import admin
from recipes.models import Ingredient, Recipe, RecipeIngredient


class MembershipInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "unit")
    search_fields = ("title",)
    list_filter = ("unit",)
    empty_value_display = "-пусто-"


class RecipeAdmin(admin.ModelAdmin):
    inlines = [MembershipInline,]

    search_fields = ("title",)
    list_filter = ("time_cooking",)
    empty_value_display = "-пусто-"


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "recipes", "ingredient", "count")
    search_fields = ("recipes", "ingredient")
    list_filter = ("count",)
    empty_value_display = "-пусто-"


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)