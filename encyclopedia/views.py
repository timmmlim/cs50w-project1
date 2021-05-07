import random
from markdown2 import Markdown

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def show_entry(request, entry):
    '''
    displays the wiki page associated with the input entry
    '''
    md = Markdown()
    entry_md = util.get_entry(entry)
    
    try:
        converted_md = md.convert(entry_md)
        return render(request, "encyclopedia/entry.html", {
            'entry': md.convert(util.get_entry(entry)),
            'entry_title': entry})

    except TypeError:
        return render(request, "encyclopedia/entry.html", {
            'entry': None})

def search_entry(request):
    '''
    returns pages whose name contains the query
    '''
    if request.method == "GET":
        query = request.GET.get("q", None)
        if query:
            entries = util.list_entries()
            results = [e for e in entries if query.lower() in e.lower()]
            return render(request, "encyclopedia/search.html", {'entries': results, "query": query})

def create_entry(request):
    '''
    creates a new wiki entry
    '''
    return render(request, "encyclopedia/new_entry.html")

def submit_entry(request):
    '''
    submits a newly created wiki entry
    '''
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        stripped_title = title.strip()

    if not util.get_entry(title):
        util.save_entry(stripped_title, content)
        return index(request)
    else:
        return render(request, "encyclopedia/error.html", {"title": stripped_title})

def delete_entry(request, entry_title):
    '''
    deletes the entry_title from the server
    '''
    util.delete_entry(entry_title)
    return render(request, "encyclopedia/delete.html", {"title": entry_title})


def render_edit_page(request, entry_title):
    '''
    helper method to render the edit page
    '''
    return render(request, 'encyclopedia/edit_entry.html', {'title': entry_title, 'content': util.get_entry(entry_title)})


def update_entry(request):
    '''
    overwrites existing entries in the server
    '''
    if request.method == 'POST':
        title = request.POST['title']
        new_content = request.POST['content']

    # delete the old entry
    util.delete_entry(title)

    # save the new entry instead
    util.save_entry(title, new_content)
    return HttpResponseRedirect(reverse('entry', kwargs={'entry': title}))


def random_entry(request):
    '''
    renders a random wiki entry
    '''
    entries = util.list_entries()
    random_int = random.randint(0, len(entries) - 1)
    random_title = entries[random_int]
    return HttpResponseRedirect(reverse("entry", kwargs={"entry": random_title}))


