from django.db import models

from jangela.domain.enums.erreserba_egoera import ErreserbaEgoera
from jangela.domain.enums.otordu_mota import OtorduMota
from jangela.infrastructure.persistence.models.choices import enum_choices, enum_max_length


class ErreserbaModel(models.Model):
    """Erreserba puntuala."""

    erabiltzailea = models.ForeignKey(
        "jangela.ErabiltzaileaModel",
        on_delete=models.PROTECT,
        related_name="erreserbak",
    )
    erreserba_data = models.DateField()
    otordu_mota = models.CharField(
        max_length=enum_max_length(OtorduMota), choices=enum_choices(OtorduMota)
    )
    erreserba_egoera = models.CharField(
        max_length=enum_max_length(ErreserbaEgoera),
        choices=enum_choices(ErreserbaEgoera),
        default=ErreserbaEgoera.AKTIBOA.value,
    )
    sortze_data = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "erreserba"
