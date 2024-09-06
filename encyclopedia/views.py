from django.shortcuts import render, redirect
from markdown2 import Markdown
import random

from . import util

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()

    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def show_entry_page(request, title):
    html_content = convert_md_to_html(title)

    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "error_message": "This page does not exist!"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        }) 

def search(request):
    if request.method == 'POST':
        search_entry = request.POST['q']
        html_content = convert_md_to_html(search_entry)
        print(html_content)

        if html_content:
            return render(request, "encyclopedia/entry.html", {
                "title": search_entry,
                "content": html_content
            })
        else:
            all_entries = util.list_entries()
            entries_by_search_substrings = []
            for entry in all_entries:
                if search_entry.lower() in entry.lower():
                    entries_by_search_substrings.append(entry)

            if entries_by_search_substrings:
                return render(request, "encyclopedia/search.html", {
                    "entries": entries_by_search_substrings
                })
            else:                  
                return render(request, "encyclopedia/search.html", {
                    "message": f"Unfortunatly there is no such page as /{search_entry}/"
                })

def new_page(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/new_page.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        title_exist = util.get_entry(title)
        action = request.POST['action']

        if action == 'Create Page':
            if title_exist:
                return render(request, "encyclopedia/error.html", {
                    "error_message": "Such a title already exist, please try another one!"
                })
            else:
                util.save_entry(title, content)

                return show_entry_page(request, title)
        else:
            return redirect('index')
        
def edit_page(request):
    if request.method == 'POST':
        title = request.POST['entry_title']
        content = util.get_entry(title)
        action = request.POST['action']
        print(action)

        if action == 'Edit':
            return render(request, "encyclopedia/edit_page.html", {
                "title": title,
                "content": content,
            })
        elif action == 'Home':
            return redirect('index')
        else:
            util.delete_entry(title)
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            }) 
    
def save_edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        action = request.POST['action']

        if action == 'Save':
            util.save_entry(title, content)
            return show_entry_page(request, title)
        else:
            return show_entry_page(request, title)

def show_random_page(request):
    all_entries = util.list_entries()
    random_entry = random.choice(all_entries)
    
    return show_entry_page(request, random_entry)
