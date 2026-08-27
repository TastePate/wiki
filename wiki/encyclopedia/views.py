from django.shortcuts import render
from encyclopedia.util import list_entries


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": list_entries,
    })

def wiki(request, page_title):
    return render(request, "encyclopedia/index.html", {
        "page_title": page_title
    })
