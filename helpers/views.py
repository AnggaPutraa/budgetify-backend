from django.http import HttpResponseRedirect
from django.urls import reverse

def handle_404_not_found(request, exception):
    return HttpResponseRedirect(reverse("admin:index"))