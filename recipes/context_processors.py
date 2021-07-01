from urllib.parse import urlencode

from .models import Tag, Follow


def shoplist(request):
    cart = request.session.setdefault('cart', {})
    return {'cart': cart}


def tags(request):
    tags_ = Tag.objects.all()
    currently_selected_tags = request.GET.getlist('tags', [])
    filtered_tags = currently_selected_tags or [tag.slug for tag in tags_]

    result = []
    for tag in tags_:
        active = tag.slug in filtered_tags
        tags_in_query = filtered_tags.copy()
        if active:
            tags_in_query.remove(tag.slug)
        else:
            tags_in_query.append(tag.slug)

        query_string = urlencode({'tags': tags_in_query}, doseq=True)
        tag_info = {
            'slug': tag.slug,
            'name': tag.name,
            'color': tag.color,
            'active': active,
            'href': f'{request.path}?{query_string}',
        }
        result.append(tag_info)

    return {
        'tags': result,
        'currently_selected_tags_query': urlencode(
            {'tags': currently_selected_tags}, doseq=True,
        ),
    }


def is_following(request):
    if not request.user.is_authenticated:
        return {'follows': ''}
    follower = request.user
    follows = []
    for follow in Follow.objects.filter(user=follower):
        follows.append(follow.author.username)
    return {'follows': follows}

