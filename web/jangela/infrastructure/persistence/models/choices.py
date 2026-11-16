from enum import Enum


def enum_choices(enum_klasea: type[Enum]) -> list[tuple[str, str]]:
    """Domeinuko enum batetik Django-ren choices zerrenda sortzen du."""
    return [(balioa.value, balioa.name) for balioa in enum_klasea]


def enum_max_length(enum_klasea: type[Enum]) -> int:
    """Enum-eko baliorik luzeenaren luzera (CharField-en max_length-erako)."""
    return max(len(balioa.value) for balioa in enum_klasea)
