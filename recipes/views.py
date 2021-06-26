import io
import sys
import pdfkit
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView

from .forms import RecipeForm
from .models import Recipe, User, RecipeIngredient


def filter_by_tags(request, qs):
    """Filtration by tags"""
    tags = request.GET.getlist('tags', [])
    if tags:
        qs = qs.filter(tags__slug__in=tags).distinct()
        return qs
    else:
        return qs


class IsFavoriteMixin:
    """Add annotation with favorite mark to the View."""

    def get_queryset(self):
        """Add annotation with favorite mark."""
        qs = super().get_queryset()
        qs = (
            qs
            .select_related('author')
            .with_is_favorite(user_id=self.request.user.id)
        )

        return qs


class BaseRecipeListView(IsFavoriteMixin, ListView):
    """Base view for Recipe list."""
    context_object_name = 'recipe_list'
    queryset = Recipe.objects.all()
    paginate_by = 6
    page_title = None

    def get_context_data(self, **kwargs):
        """Add page title to the context."""
        kwargs.update({
            'page_title': self._get_page_title(),
        })

        context = super().get_context_data(**kwargs)
        return context

    def _get_page_title(self):
        """Get page title."""
        assert self.page_title, f'Attribute "page_title" not set for' \
                                f' {self.__class__.__name__}' # noqa

        return self.page_title


class IndexView(BaseRecipeListView):
    """Main page that displays list of Recipes."""
    page_title = 'Рецепты'
    template_name = 'recipes/recipe_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return filter_by_tags(self.request, qs)


class FavoriteView(LoginRequiredMixin, BaseRecipeListView):
    """List of current user's favorite Recipes"""
    page_title = 'Избранное'
    template_name = 'recipes/recipe_list.html'

    def get_queryset(self):
        """Display favorite recipes only."""
        qs = super().get_queryset()
        user = self.request.user
        qs = qs.filter(favorites__user=user).with_is_favorite(user_id=user.id)
        return filter_by_tags(self.request, qs)


class ProfileView(BaseRecipeListView):
    """User's page with its name and list of authored Recipes."""
    template_name = 'recipes/profile_recipe_list.html'

    def get(self, request, *args, **kwargs):
        """Store 'user' parameter for data filtration purposes."""
        self.user = get_object_or_404(User, username=kwargs.get('username'))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """Display favorite recipes only."""
        qs = super().get_queryset()
        qs = qs.filter(author=self.user)
        return filter_by_tags(self.request, qs)

    def _get_page_title(self):
        """Get page title."""
        return self.user.get_full_name()

    def get_context_data(self, **kwargs):
        """Adding Author to context."""
        kwargs.update({'author': self.user})
        context = super().get_context_data(**kwargs)
        return context


class RecipeDetailView(IsFavoriteMixin, DetailView):
    """Page with Recipe details."""
    queryset = Recipe.objects.all()
    template_name = 'recipes/recipe_detail.html'

    def get_queryset(self):
        """Display favorite recipes only."""
        qs = super().get_queryset()
        qs = (
            qs
            .prefetch_related('recipe_ingredients__ingredient')
            .with_is_favorite(user_id=self.request.user.id)
        )

        return qs


class SubscriptionView(BaseRecipeListView):
    """Page that displays list of Recipes from subscriptions."""
    page_title = 'Мои подписки'
    template_name = 'recipes/my_follows.html'

    def get_queryset(self):
        """Display following recipes only."""
        users = User.objects.all()
        qs = users.filter(following__user_id=self.request.user.id)
        return qs


def cart(request):
    """Rendering shopping cart."""
    page_title = 'Список покупок'

    return render(
        request,
        'recipes/cart.html',
        {'page_title': page_title}
    )


def download_cart(request):
    """Download ingredients to buy.
    wkhtmltopdf Required!!!"""
    recipes_dict = request.session.get('cart')
    recipe_ingredients = RecipeIngredient.objects.filter(
        recipe__in=recipes_dict.keys()
    )
    recipe_ingredients = recipe_ingredients.values(
        'ingredient__title', 'ingredient__dimension'
    ).annotate(Sum('amount', distinct=True))
    rendered = render_to_string(
        'recipes/download_cart.html',
        {'recipe_ingredients': recipe_ingredients}
    )
    if sys.platform == 'win32':
        config = pdfkit.configuration(
            wkhtmltopdf='D:\\DEV\\foodgram\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
        )
        file = pdfkit.from_string(rendered, False, configuration=config)
    else:
        file = pdfkit.from_string(rendered, False)
    buffer = io.BytesIO(file)
    return FileResponse(buffer, as_attachment=True, filename='cart_file.pdf')


@login_required
def recipe_edit_or_create(request, recipe_id=None):
    recipe = None
    if recipe_id is not None:
        recipe = get_object_or_404(Recipe, pk=recipe_id, author=request.user)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)

    form = RecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=recipe,
    )

    if request.method == 'POST' and form.is_valid():
        form.instance.author = request.user
        recipe = form.save()
        return redirect('recipe', pk=recipe.pk)

    return render(
        request,
        'recipes/recipe_edit_or_create.html',
        {'form': form,
         'is_edit': recipe is not None,
         'ingredients': ingredients, },
    )


@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, author=request.user)
    recipe.delete()
    return redirect('index')


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )
