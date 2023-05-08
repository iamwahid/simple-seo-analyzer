from django.shortcuts import render
from django.conf import settings
from .forms import UrlForm
from . import utils 
from .models import Url
import json
import os

def check_url(request):
    if request.method == "POST":
        form = UrlForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            output = utils.analyze_site(url)
            context = output
            context.update({"form": form})
            return render(request, "url-form.html", context=context)
    else:
        form = UrlForm()

    return render(request, "url-form.html", {"form": form})