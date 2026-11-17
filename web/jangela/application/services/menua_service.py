from datetime import date

from django.db import IntegrityError, transaction
from django.db.models import Case, IntegerField, When
from django.shortcuts import get_object_or_404

from jangela.domain.enums.otordu_mota import OtorduMota
from jangela.models import MenuaModel

BIKOIZTUTA_MEZUA = "Badago menu bat data eta otordu mota horrekin (11. araua)."


class MenuaBikoiztutaError(Exception):
    """11. araua: data + otordu mota bakoitzeko menu bakarra."""


class MenuaService:
    """Menuen negozio-logika (UC15–UC17). ORM zuzenean erabiltzen du."""

    @staticmethod
    def list():
        """Menu guztiak, data gorantz eta egunean GOSARIA → BAZKARIA → AFARIA."""
        # Otordu moten ordena enum-etik (ez alfabetikoa)
        ordena = Case(
            *[When(otordu_mota=mota.value, then=i) for i, mota in enumerate(OtorduMota)],
            output_field=IntegerField(),
        )
        return MenuaModel.objects.order_by("menua_data", ordena)

    @staticmethod
    def lortu(pk: int) -> MenuaModel:
        """Menua id-aren arabera; ez badago, 404."""
        # Erroreen kudeaketa: menurik ez -> 404
        return get_object_or_404(MenuaModel, pk=pk)

    @staticmethod
    def create(menua_data: date, otordu_mota: str, deskribapena: str,
               aukera_beganoa: str) -> MenuaModel:
        """UC15: menu berria sortu."""
        menua = MenuaModel(menua_data=menua_data, otordu_mota=otordu_mota,
                           deskribapena=deskribapena, aukera_beganoa=aukera_beganoa)
        MenuaService._gorde(menua)
        return menua

    @staticmethod
    def update(menua: MenuaModel, menua_data: date, otordu_mota: str,
               deskribapena: str, aukera_beganoa: str) -> MenuaModel:
        """UC16: menua eguneratu."""
        menua.menua_data = menua_data
        menua.otordu_mota = otordu_mota
        menua.deskribapena = deskribapena
        menua.aukera_beganoa = aukera_beganoa
        MenuaService._gorde(menua)
        return menua

    @staticmethod
    def delete(menua: MenuaModel) -> None:
        """UC17: menua ezabatu (Menuak ez du erlaziorik)."""
        menua.delete()

    @staticmethod
    def _gorde(menua: MenuaModel) -> None:
        # Negozio-araua (11. araua): data + otordu mota bakoitzeko menu bakarra.
        # Editatzean, menua bera ez da kontuan hartzen.
        # SQL injection saihestu: ORM / parametrizazioa
        badago = (MenuaModel.objects
                  .filter(menua_data=menua.menua_data, otordu_mota=menua.otordu_mota)
                  .exclude(pk=menua.pk)
                  .exists())
        if badago:
            raise MenuaBikoiztutaError(BIKOIZTUTA_MEZUA)
        # Azken babesa: datu-baseko UniqueConstraint (aldi bereko eskaerak)
        try:
            with transaction.atomic():
                menua.save()
        except IntegrityError:
            raise MenuaBikoiztutaError(BIKOIZTUTA_MEZUA)
