from django.shortcuts import render
from django.http import Http404, HttpResponse

# This function runs when someone goes to the main page "/"
# → Django finds the file index.html, reads it, and sends the complete page to the user
def index (request):
    return render(request, "singlepage/index.html")

# A simple list with 3 texts (like a menu with 3 dishes)
# texts[0] = first text, texts[1] = second, texts[2] = third
texts = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus ac magna eu enim tincidunt varius. Sed euismod libero non purus faucibus, vel hendrerit arcu ullamcorper.",
    "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis.",
    "At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi."
]

# This function runs when someone goes to /sections/1 or /sections/2 etc.
def section(request, num):
    if 1 <= num <= 3:
        return HttpResponse(texts[num-1])
    else:
        raise Http404("No such section")
