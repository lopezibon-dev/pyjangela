from django.db import models


class IkasturtekoErreserbaModel(models.Model):
    """Ikasle egoiliarraren asteko agenda (4., 12. eta 13. arauak).

    Markatutako otorduak markatutako egunetan aplikatzen dira (egun eta otordu).
    """

    ikaslea = models.OneToOneField(
        "jangela.IkasleaModel",
        on_delete=models.PROTECT,
        related_name="ikasturteko_erreserba",
    )
    # Otorduak
    gosaria = models.BooleanField(default=False)
    bazkaria = models.BooleanField(default=False)
    afaria = models.BooleanField(default=False)
    # Egunak
    astelehena = models.BooleanField(default=False)
    asteartea = models.BooleanField(default=False)
    asteazkena = models.BooleanField(default=False)
    osteguna = models.BooleanField(default=False)
    ostirala = models.BooleanField(default=False)
    larunbata = models.BooleanField(default=False)
    igandea = models.BooleanField(default=False)

    class Meta:
        db_table = "ikasturteko_erreserba"
