from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from jangela.domain.enums.rola import Rola


def rola_behar(rola: Rola):
    """Rol-dekoratzailea: Laravel-eko rol middleware-aren baliokidea.

    Saiorik gabe -> login-era (login_required). Beste rol batekin -> 403.
    """

    def dekoratzailea(view):
        @wraps(view)
        @login_required
        def bilgarria(request, *args, **kwargs):
            # Negozio-araua: rol bakoitzak bere bistak soilik (2. araua)
            if request.user.rola != rola.value:
                raise PermissionDenied
            return view(request, *args, **kwargs)

        return bilgarria

    return dekoratzailea
