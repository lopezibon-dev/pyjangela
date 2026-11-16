from django.db import models
from django.db.models import Q

from jangela.domain.enums.ordainketa_egoera import OrdainketaEgoera
from jangela.domain.enums.ordainketa_mota import OrdainketaMota
from jangela.infrastructure.persistence.models.choices import enum_choices, enum_max_length


class OrdainketaModel(models.Model):
    """Ordainketa: beti erabiltzaile bati dagokio (7. araua)."""

    erabiltzailea = models.ForeignKey(
        "jangela.ErabiltzaileaModel",
        on_delete=models.PROTECT,
        related_name="ordainketak",
    )
    # ALDIZKAKOA denean bakarrik (8. araua)
    erreserba = models.OneToOneField(
        "jangela.ErreserbaModel",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="ordainketa",
    )
    ordainketa_mota = models.CharField(
        max_length=enum_max_length(OrdainketaMota), choices=enum_choices(OrdainketaMota)
    )
    zenbatekoa = models.DecimalField(max_digits=8, decimal_places=2)
    egoera = models.CharField(
        max_length=enum_max_length(OrdainketaEgoera),
        choices=enum_choices(OrdainketaEgoera),
        default=OrdainketaEgoera.ORDAINTZEKE.value,
    )
    # Sortze data derrigorrezkoa (10. araua)
    sortze_data = models.DateTimeField(auto_now_add=True)
    ordainketa_data = models.DateTimeField(null=True, blank=True)
    azalpena = models.TextField(blank=True)

    class Meta:
        db_table = "ordainketa"
        constraints = [
            # 8. araua: ALDIZKAKOA -> erreserba bai; HILEKOA -> erreserba NULL
            models.CheckConstraint(
                condition=(
                    Q(ordainketa_mota=OrdainketaMota.ALDIZKAKOA.value, erreserba__isnull=False)
                    | Q(ordainketa_mota=OrdainketaMota.HILEKOA.value, erreserba__isnull=True)
                ),
                name="ordainketa_mota_erreserba_ck",
            ),
            # 9. araua: ORDAINDUTA -> ordainketa_data bai; ORDAINTZEKE -> NULL
            models.CheckConstraint(
                condition=(
                    Q(egoera=OrdainketaEgoera.ORDAINDUTA.value, ordainketa_data__isnull=False)
                    | Q(egoera=OrdainketaEgoera.ORDAINTZEKE.value, ordainketa_data__isnull=True)
                ),
                name="ordainketa_egoera_data_ck",
            ),
        ]
