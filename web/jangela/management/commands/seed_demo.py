from django.core.management.base import BaseCommand
from django.db import transaction

from jangela.domain.enums.rola import Rola
from jangela.models import (
    ErabiltzaileaModel,
    ErreserbaModel,
    IkasleaModel,
    IkasturtekoErreserbaModel,
    OrdainketaModel,
)

PASAHITZA = "1234"

# Demo-erabiltzaileak: datu guztiak asmatuak dira (errepoa publikoa da).
# egoiliarra: None -> ez du Ikaslea erregistrorik (3. araua)
ERABILTZAILEAK = [
    {"email": "iker@jangela.eus", "izena": "Iker", "abizenak": "Egoiliar",
     "rola": Rola.IKASLEA, "egoiliarra": True, "aktiboa": True},
    {"email": "maite@jangela.eus", "izena": "Maite", "abizenak": "Ikaslea",
     "rola": Rola.IKASLEA, "egoiliarra": False, "aktiboa": True},
    {"email": "jon@jangela.eus", "izena": "Jon", "abizenak": "Irakaslea",
     "rola": Rola.IRAKASLEA, "egoiliarra": None, "aktiboa": True},
    {"email": "david@jangela.eus", "izena": "David", "abizenak": "Sukaldea",
     "rola": Rola.SUKALDEA, "egoiliarra": None, "aktiboa": True},
    # Erabiltzaile inaktiboa: ezin du saioa hasi (19. araua)
    {"email": "mikel@jangela.eus", "izena": "Mikel", "abizenak": "Inaktibo",
     "rola": Rola.IRAKASLEA, "egoiliarra": None, "aktiboa": False},
]


class Command(BaseCommand):
    help = "Demo-datuak ezabatu eta berriro sortzen ditu (idenpotentea)."

    def handle(self, *args, **options):
        with transaction.atomic():
            self.ezabatu()
            self.sortu()
        self.stdout.write(self.style.SUCCESS(
            f"{len(ERABILTZAILEAK)} demo-erabiltzaile sortuta (pasahitza: {PASAHITZA})."
        ))

    def ezabatu(self):
        """Demo-erabiltzaileak eta haien datuak ezabatu (beste erabiltzaileak ez)."""
        emailak = [e["email"] for e in ERABILTZAILEAK]
        # PROTECT dela eta, umeak lehenago ezabatu behar dira
        IkasturtekoErreserbaModel.objects.filter(
            ikaslea__erabiltzailea__email__in=emailak
        ).delete()
        OrdainketaModel.objects.filter(erabiltzailea__email__in=emailak).delete()
        ErreserbaModel.objects.filter(erabiltzailea__email__in=emailak).delete()
        IkasleaModel.objects.filter(erabiltzailea__email__in=emailak).delete()
        ErabiltzaileaModel.objects.filter(email__in=emailak).delete()

    def sortu(self):
        for datuak in ERABILTZAILEAK:
            # create_user-ek pasahitza hash moduan gordetzen du (1. araua)
            erabiltzailea = ErabiltzaileaModel.objects.create_user(
                email=datuak["email"],
                password=PASAHITZA,
                first_name=datuak["izena"],
                last_name=datuak["abizenak"],
                rola=datuak["rola"].value,
                is_active=datuak["aktiboa"],
            )
            # IKASLEA rolekoek soilik dute Ikaslea erregistroa (3. araua)
            if datuak["rola"] == Rola.IKASLEA:
                IkasleaModel.objects.create(
                    erabiltzailea=erabiltzailea, egoiliarra=datuak["egoiliarra"]
                )
