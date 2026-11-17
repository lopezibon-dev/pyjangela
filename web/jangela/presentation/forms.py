from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from jangela.models import ErabiltzaileaModel


class SaioaHasiForm(AuthenticationForm):
    """Login formularioa: emaila + pasahitza (USERNAME_FIELD = "email")."""

    error_messages = {
        **AuthenticationForm.error_messages,
        "inactive": "Kontu hau ez dago aktibo: ezin duzu saioa hasi.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for eremua in self.fields.values():
            eremua.widget.attrs["class"] = "form-control"

    # Sarreren balidazioa (formularioa)
    def clean(self):
        # 19. araua: ModelBackend-ek ez ditu inaktiboak autentifikatzen, baina
        # mezu orokorra ematen du. Pasahitza zuzena bada, mezu argia erakutsi.
        email = self.cleaned_data.get("username")
        pasahitza = self.cleaned_data.get("password")
        if email and pasahitza:
            # SQL injection saihestu: ORM / parametrizazioa
            erabiltzailea = ErabiltzaileaModel.objects.filter(email=email).first()
            if (erabiltzailea and not erabiltzailea.is_active
                    and erabiltzailea.check_password(pasahitza)):
                raise ValidationError(self.error_messages["inactive"], code="inactive")
        return super().clean()
