import time   # This lets us pause the code (like waiting 1 second) — only for demo
from django.http import JsonResponse # Tool to send JSON data (perfect for JavaScript)
from django.shortcuts import render # Tool to show normal HTML pages

def index(request):  # This function runs when someone goes to the main page "/"
    return render(request, "posts/index.html")  # → Django finds the file index.html and sends the complete page to the browser

def posts(request):  # → Django finds the file index.html and sends the complete page to the browser # Example URL: /posts?start=1&end=10
    start = int(request.GET.get("start") or 0) # Get the "start" number from the URL, or use 0 if missing 
    # Example: /posts?start=5 → start = 5 # If no start → start = 0              
    end = int(request.GET.get("end") or (start + 9)) 
    # Get the "end" number, or calculate it as start + 9 # Example: if start=1 → end = 10
    data = []
    for i in range(start, end + 1):
        data.append(f"Post #{i}")

    time.sleep(1)

    # Send the data back as JSON
    # JavaScript will receive: {"posts": ["Post #1", "Post #2", ...]}
    return JsonResponse({
        "posts": data
    })    


