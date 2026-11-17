from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from jangela.domain.enums.rola import Rola
from jangela.presentation.decorators import rola_behar

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
