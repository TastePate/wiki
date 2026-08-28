from django import forms
from django.http import HttpRequest
from django.contrib import messages
from django.shortcuts import render, redirect
from encyclopedia.util import list_entries, get_entry, save_entry
from markdown2 import Markdown
from random import choice

class NewArticleForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)


class NewEditForm(forms.Form):
    new_content = forms.CharField(label="Edit Article's Content", widget=forms.Textarea)


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
                return redirect("encyclopedia:wiki", page_title=title)
            else:
                messages.error(request, f"An article with name {title} already exists!")

    return render(request, "encyclopedia/add.html", {
        "form": NewArticleForm(),
    })

def edit(request: HttpRequest, page_title):
    old_content = get_entry(page_title)
    if request.method == "POST":
        form = NewEditForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data["new_content"]
            save_entry(page_title, new_content)
            return redirect("encyclopedia:wiki", page_title=page_title)

    return render(request, "encyclopedia/edit.html", {
        "page_title": page_title,
        "form": NewEditForm(initial={
            "new_content": old_content
        })
    })

def random(request: HttpRequest):
    entries = list_entries()
    random_page = choice(entries)
    return redirect("encyclopedia:wiki", page_title=random_page)


def search(request: HttpRequest):
    search_input = request.GET.get("q").lower()
    entries = list_entries()
    result = []
    for entry in entries:
        if search_input == entry.lower():
            return redirect("encyclopedia:wiki", page_title=search_input)
        if search_input in entry.lower():
            result.append(entry)

    return render(request, "encyclopedia/search.html", {
        "entries": result,
        "search_input": search_input
    })


