from django import template

register = template.Library()

@register.filter
def replace_titles(titolo_film):
    # Filtro creato per risolvere il problema degli spazi nei titoli dei film,
    # Si è preferito usare un _ per gestire l'utilizzo dei titolo dei film negli URL.

    return titolo_film.replace("_"," ")