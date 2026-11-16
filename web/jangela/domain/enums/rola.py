from enum import Enum


class Rola(str, Enum):
    """Erabiltzailearen rola (erabiltzaile bakoitzak rol bakarra)."""

    IKASLEA = "IKASLEA"
    IRAKASLEA = "IRAKASLEA"
    SUKALDEA = "SUKALDEA"
