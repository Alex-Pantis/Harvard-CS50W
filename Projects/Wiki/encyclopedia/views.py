from django.shortcuts import render, redirect
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"Page '{title}' not found"
        })
    
    import markdown2
    html_content = markdown2.markdown(content)
    
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })

def search(request):
    # Step 1: Get what the user searched for
    query = request.GET.get('q', '')
    
    # Step 2: Get all encyclopedia entries
    all_entries = util.list_entries()
    
    # Step 3: Check if query exactly matches an entry
    for entry in all_entries:
        if query.lower() == entry.lower():
            # Exact match! Send user directly to that page
            return redirect('entry', title=entry)
    
    # Step 4: No exact match, find entries containing the query
    matching_entries = []
    for entry in all_entries:
        if query.lower() in entry.lower():
            matching_entries.append(entry)
    
    # Step 5: Show search results page
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "entries": matching_entries
    })