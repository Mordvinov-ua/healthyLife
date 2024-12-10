from django import template

register = template.Library()

@register.filter
def unique_categories(groups):
    seen_categories = set()
    unique_groups = []

    for group in groups:
        if group.category not in seen_categories:
            unique_groups.append(group)
            seen_categories.add(group.category)
    
    return unique_groups