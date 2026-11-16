from django.db import models


class IkasleaModel(models.Model):
    """IKASLEA rola duen erabiltzailearen datuak (3. araua)."""

    erabiltzailea = models.OneToOneField(
        "jangela.ErabiltzaileaModel",
        on_delete=models.PROTECT,
        related_name="ikaslea",
    )
    egoiliarra = models.BooleanField(default=False)

    class Meta:
        db_table = "ikaslea"
