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
            # with open(os.path.join(settings.BASE_DIR, "seo", "output.json"), "w") as f:
            #     json.dump(output, f, indent=4, sort_keys=True)
            # obj, created = Url.objects.get_or_create(url=url, defaults={"output": json.dumps(output)})
            context = output
            context.update({"form": form})
            return render(request, "url-form.html", context=context)
    else:
        form = UrlForm()

    return render(request, "url-form.html", {"form": form})