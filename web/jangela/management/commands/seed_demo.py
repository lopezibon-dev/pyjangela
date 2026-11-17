from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from jangela.domain.enums.otordu_mota import OtorduMota
from jangela.domain.enums.rola import Rola
from jangela.models import (
    ErabiltzaileaModel,
    ErreserbaModel,
    IkasleaModel,
    IkasturtekoErreserbaModel,
    MenuaModel,
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


# Demo-menuak: gaur-3 egunetik gaur+7 egunera, otordu mota guztiekin.
MENU_EGUNAK = range(-3, 8)
# (deskribapena, aukera_beganoa). None -> beganoa = deskribapena (17. araua)
MENUAK = {
    OtorduMota.GOSARIA: [
        ("Ogi txigortua tomatearekin eta olioarekin, fruta", None),
        ("Jogurta, muesli-a eta laranja-zukua", "Soja-jogurta, muesli-a eta laranja-zukua"),
        ("Kafesnea, gailetak eta sagarra", "Oloa-esnea, gailetak eta sagarra"),
    ],
    OtorduMota.BAZKARIA: [
        ("Dilista-zopa eta oilaskoa piperrekin", "Dilista-zopa eta tofua piperrekin"),
        ("Entsalada mistoa eta legatza saltsa berdean", "Entsalada mistoa eta garbantzu-hanburgesa"),
        ("Makarroiak tomatearekin eta txerri-xerra", "Makarroiak tomatearekin eta seitan-xerra"),
        ("Barazki-paella eta fruta", None),
    ],
    OtorduMota.AFARIA: [
        ("Barazki-krema eta tortilla", "Barazki-krema eta barazki-salteatua"),
        ("Porrusalda eta bakailaoa", "Porrusalda eta onddo-xerrak"),
        ("Arroz-entsalada eta fruta", None),
    ],
}


class Command(BaseCommand):
    help = "Demo-datuak ezabatu eta berriro sortzen ditu (idenpotentea)."

    def handle(self, *args, **options):
        with transaction.atomic():
            self.ezabatu()
            self.sortu()
            menu_kopurua = self.menuak_sortu()
        self.stdout.write(self.style.SUCCESS(
            f"{len(ERABILTZAILEAK)} demo-erabiltzaile sortuta (pasahitza: {PASAHITZA})."
        ))
        self.stdout.write(self.style.SUCCESS(f"{menu_kopurua} demo-menu sortuta."))

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

    def menuak_sortu(self) -> int:
        """Demo-tarteko menuak ezabatu eta berriro sortu (tartetik kanpokoak ez)."""
        gaur = timezone.localdate()
        egunak = [gaur + timedelta(days=n) for n in MENU_EGUNAK]
        MenuaModel.objects.filter(menua_data__range=(egunak[0], egunak[-1])).delete()
        menuak = []
        for i, eguna in enumerate(egunak):
            for mota, aukerak in MENUAK.items():
                deskribapena, beganoa = aukerak[i % len(aukerak)]
                menuak.append(MenuaModel(
                    menua_data=eguna,
                    otordu_mota=mota.value,
                    deskribapena=deskribapena,
                    aukera_beganoa=beganoa or deskribapena,
                ))
        MenuaModel.objects.bulk_create(menuak)
        return len(menuak)
