def filter_by_tags(request, qs):
    """Filtration by tags"""
    tags = request.GET.getlist('tags', [])
    if tags:
        qs = qs.filter(tags__slug__in=tags).distinct()
        return qs
    else:
        return qs
