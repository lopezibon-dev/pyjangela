from django.db import models

from jangela.domain.enums.otordu_mota import OtorduMota
from jangela.infrastructure.persistence.models.choices import enum_choices, enum_max_length


class MenuaModel(models.Model):
    """Eguneko otordu baten menua: estandarra eta beganoa (17. araua)."""

    menua_data = models.DateField()
    otordu_mota = models.CharField(
        max_length=enum_max_length(OtorduMota), choices=enum_choices(OtorduMota)
    )
    deskribapena = models.TextField()
    aukera_beganoa = models.TextField()

    class Meta:
        db_table = "menua"
        constraints = [
            # 11. araua: menu bakarra data eta otordu mota bakoitzeko
            models.UniqueConstraint(
                fields=["menua_data", "otordu_mota"],
                name="menua_data_otordu_mota_uq",
            ),
        ]
