from django import forms

from .models import Recipe, Tag, Ingredient, RecipeIngredient


class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), to_field_name='slug',
    )
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        to_field_name='name',
        required=False,
        label='Ингредиенты'
    )
    _ingredients = {}

    class Meta:
        model = Recipe
        fields = (
            'name',
            'tags',
            'ingredients',
            'time_for_preparing',
            'description',
            'image',
        )

    def clean(self):
        data = self.cleaned_data
        ingredients = {}

        for key, value in self.data.items():
            if not key.startswith('nameIngredient_'):
                continue
            idx = key.replace('nameIngredient_', '')
            ingredient_name = value
            ingredient_value = self.data[f'valueIngredient_{idx}']
            ingredients[ingredient_name] = ingredient_value

        if not ingredients:
            raise forms.ValidationError(
                {
                    'ingredients': [
                        'Необходимо добавить хотя бы один ингредиент',
                    ]
                }
            )

        self._ingredients = ingredients

        return data

    def save(self, commit=True):
        recipe = super().save()

        recipe.ingredients.all().delete()

        for name, amount in self._ingredients.items():
            try:
                ingredient = Ingredient.objects.get(title=name)
            except Ingredient.DoesNotExist:
                continue

            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount
            )
        return recipe
