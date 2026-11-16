# Django-k ORM ereduak erregistra ditzan (migrazioak sortzeko)
from jangela.infrastructure.persistence.models.erabiltzailea import ErabiltzaileaModel
from jangela.infrastructure.persistence.models.erreserba import ErreserbaModel
from jangela.infrastructure.persistence.models.ikaslea import IkasleaModel
from jangela.infrastructure.persistence.models.ikasturteko_erreserba import IkasturtekoErreserbaModel
from jangela.infrastructure.persistence.models.menua import MenuaModel
from jangela.infrastructure.persistence.models.ordainketa import OrdainketaModel

__all__ = [
    "ErabiltzaileaModel",
    "IkasleaModel",
    "IkasturtekoErreserbaModel",
    "ErreserbaModel",
    "OrdainketaModel",
    "MenuaModel",
]
