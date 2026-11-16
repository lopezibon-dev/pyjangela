from django.shortcuts import render


def hasiera(request):
    """Hasierako orri publikoa."""
    return render(request, "hasiera.html")
