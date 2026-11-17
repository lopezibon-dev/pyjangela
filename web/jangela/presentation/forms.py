from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from jangela.domain.enums.otordu_mota import OtorduMota
from jangela.infrastructure.persistence.models.choices import enum_choices
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


class MenuaForm(forms.Form):
    """Menua sortu/eguneratu (UC15/UC16). Sarrerako DTO-a da.

    11. araua (menu bikoiztua) MenuaService-n egiaztatzen da.
    """

    # Sarreren balidazioa (formularioa): eremu guztiak derrigorrezkoak
    menua_data = forms.DateField(
        label="Data",
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
    )
    otordu_mota = forms.ChoiceField(label="Otordu mota", choices=enum_choices(OtorduMota))
    # 17. araua: bi deskribapenak derrigorrezkoak (strip: zuriuneak soilik -> hutsik)
    deskribapena = forms.CharField(
        label="Deskribapena (menu estandarra)", widget=forms.Textarea(attrs={"rows": 3})
    )
    aukera_beganoa = forms.CharField(
        label="Aukera beganoa", widget=forms.Textarea(attrs={"rows": 3})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for izena, eremua in self.fields.items():
            klasea = "form-select" if izena == "otordu_mota" else "form-control"
            eremua.widget.attrs["class"] = klasea
