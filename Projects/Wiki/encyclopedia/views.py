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

def new_page(request):
    # Check if user is submitting the form
    if request.method == "POST":
        # Get data from the form
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        # Check if entry already exists
        if util.get_entry(title) is not None:
            # Entry exists! Show error
            return render(request, "encyclopedia/new.html", {
                "error": "An entry with this title already exists!",
                "title": title,
                "content": content
            })
        
        # Save the new entry
        util.save_entry(title, content)
        
        # Redirect to the new entry's page
        return redirect('entry', title=title)
    
    # User is just viewing the form (GET request)
    return render(request, "encyclopedia/new.html")

def edit_page(request, title):
    # Check if user is submitting edits
    if request.method == "POST":
        # Get the new content
        content = request.POST.get('content')
        
        # Save it (overwrites existing file)
        util.save_entry(title, content)
        
        # Redirect back to the entry page
        return redirect('entry', title=title)
    
    # User is viewing the edit form
    # Get current content of the entry
    content = util.get_entry(title)
    
    # Check if entry exists
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"Cannot edit '{title}' because it doesn't exist."
        })
    
    # Show edit form with current content
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })