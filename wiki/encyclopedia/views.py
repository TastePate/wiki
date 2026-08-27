from django import forms
from django.http import HttpRequest
from django.contrib import messages
from django.shortcuts import render, redirect
from encyclopedia.util import list_entries, get_entry, save_entry
from markdown2 import Markdown

class NewArticleForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)


def index(request: HttpRequest):
    return render(request, "encyclopedia/index.html", {
        "entries": list_entries,
    })

def wiki(request: HttpRequest, page_title):
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

def add(request: HttpRequest):
    if request.method == "POST":
        form = NewArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title not in list_entries():
                save_entry(title, content)
                return redirect(f"encyclopedia:wiki", page_title=title)
            else:
                messages.error(request, f"An article with name {title} already exists!")

    return render(request, "encyclopedia/add.html", {
        "form": NewArticleForm(),
    })


