from herbs.models import Tovar
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


def q_search(query):
    vector = SearchVector("title", "content")
    query = SearchQuery(query)

    return Tovar.objects.annotate(rank=SearchRank(vector,query)).filter(rank__gt=0).order_by("-rank")

