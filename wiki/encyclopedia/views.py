from django.shortcuts import render
from encyclopedia.util import list_entries, get_entry
from markdown2 import Markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": list_entries,
    })

def wiki(request, page_title):
    entry = get_entry(page_title)
    if entry:
        markdowner = Markdown()
        return render(request, "encyclopedia/page.html", {
            "page_title": page_title,
            "content": markdowner.convert(entry)
        })
    else:
         return render(request, "encyclopedia/not_found.html", {
             "page_title": page_title
         })
