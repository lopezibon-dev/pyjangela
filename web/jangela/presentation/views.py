from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_GET

from jangela.application.services.menua_service import MenuaBikoiztutaError, MenuaService
from jangela.domain.enums.rola import Rola
from jangela.presentation.decorators import rola_behar
from jangela.presentation.forms import MenuaForm

# Login ondoren, rol bakoitzaren dashboard-a (ez egoiliarra-ren arabera)
DASHBOARDAK = {
    Rola.IKASLEA.value: "ikaslea_dashboard",
    Rola.IRAKASLEA.value: "irakaslea_dashboard",
    Rola.SUKALDEA.value: "sukaldea_dashboard",
}


def hasiera(request):
    """Hasierako orri publikoa."""
    return render(request, "hasiera.html")


@login_required
def dashboard(request):
    """Erabiltzailea bere rolaren dashboard-era bideratu (LOGIN_REDIRECT_URL)."""
    # Superuser-a kontu teknikoa da: /admin/ soilik
    if request.user.is_superuser:
        return redirect("admin:index")
    return redirect(DASHBOARDAK.get(request.user.rola, "hasiera"))


@rola_behar(Rola.IKASLEA)
def ikaslea_dashboard(request):
    """IKASLEA dashboard-a (egoiliarra izan ala ez)."""
    return render(request, "ikaslea/dashboard.html")


@rola_behar(Rola.IRAKASLEA)
def irakaslea_dashboard(request):
    """IRAKASLEA dashboard-a."""
    return render(request, "irakaslea/dashboard.html")


@rola_behar(Rola.SUKALDEA)
def sukaldea_dashboard(request):
    """SUKALDEA dashboard-a (UC13, oraingoz hutsik)."""
    return render(request, "sukaldea/dashboard.html")


# --- Menuen CRUDa (UC15–UC17): SUKALDEA soilik (beste rolek 403) ---

@rola_behar(Rola.SUKALDEA)
def menuak(request):
    """Menuen zerrenda."""
    return render(request, "sukaldea/menuak.html", {"menuak": MenuaService.list()})


@rola_behar(Rola.SUKALDEA)
def menua_sortu(request):
    """UC15: menua sortu."""
    form = MenuaForm(request.POST) if request.method == "POST" else MenuaForm()
    # Sarreren balidazioa (formularioa)
    if request.method == "POST" and form.is_valid():
        try:
            MenuaService.create(**form.cleaned_data)
        except MenuaBikoiztutaError as errorea:
            # Erroreen kudeaketa: 11. araua formularioan erakutsi (ez 500)
            form.add_error(None, str(errorea))
        else:
            messages.success(request, "Menua sortu da.")
            return redirect("menuak")
    return render(request, "sukaldea/menua_form.html", {"form": form, "izenburua": "Menua sortu"})


@rola_behar(Rola.SUKALDEA)
def menua_editatu(request, pk):
    """UC16: menua eguneratu."""
    menua = MenuaService.lortu(pk)
    if request.method == "POST":
        form = MenuaForm(request.POST)
    else:
        form = MenuaForm(initial=model_to_dict(menua))
    # Sarreren balidazioa (formularioa)
    if request.method == "POST" and form.is_valid():
        try:
            MenuaService.update(menua, **form.cleaned_data)
        except MenuaBikoiztutaError as errorea:
            # Erroreen kudeaketa: 11. araua formularioan erakutsi (ez 500)
            form.add_error(None, str(errorea))
        else:
            messages.success(request, "Menua eguneratu da.")
            return redirect("menuak")
    return render(request, "sukaldea/menua_form.html", {"form": form, "izenburua": "Menua editatu"})


@rola_behar(Rola.SUKALDEA)
def menua_ezabatu(request, pk):
    """UC17: menua ezabatu. GET -> berrespena; POST -> ezabatu (inoiz ez GET bidez)."""
    menua = MenuaService.lortu(pk)
    if request.method == "POST":
        MenuaService.delete(menua)
        messages.success(request, "Menua ezabatu da.")
        return redirect("menuak")
    return render(request, "sukaldea/menua_ezabatu.html", {"menua": menua})


# --- Menua kontsultatu (UC05/UC11): rol guztiak, irakurketa soilik ---

@rola_behar(Rola.IKASLEA, Rola.IRAKASLEA, Rola.SUKALDEA)
def menua_kontsultatu(request):
    """UC05/UC11: orria gaurko menuekin; beste datak menua.js-k kargatzen ditu (fetch)."""
    gaur = timezone.localdate()
    return render(request, "menua.html", {
        "data": gaur,
        "menuak": MenuaService.lortuEgunekoMenuak(gaur),
    })


@require_GET
@rola_behar(Rola.IKASLEA, Rola.IRAKASLEA, Rola.SUKALDEA)
def menua_json(request):
    """UC05/UC11: data bateko menuak JSON formatuan (?data=UUUU-HH-EE)."""
    # Sarreren balidazioa: data parametroa esplizituki (formatu okerra -> 400)
    try:
        data = date.fromisoformat(request.GET.get("data", ""))
    except ValueError:
        return JsonResponse({"errorea": "Data okerra: erabili UUUU-HH-EE formatua."}, status=400)

    menuak = MenuaService.lortuEgunekoMenuak(data)
    return JsonResponse({
        "data": data.isoformat(),
        # 17. araua: menu estandarra eta beganoa; null -> menurik ez
        "menuak": {
            mota: {"deskribapena": menua.deskribapena, "aukera_beganoa": menua.aukera_beganoa}
            if menua else None
            for mota, menua in menuak.items()
        },
    })
