from enum import Enum

from tps.symbols.english import LETTERS_EN
from tps.symbols.russian import LETTERS_RU, LETTERS_RU_TRANS


class Languages(str, Enum):
  en = "en"
  ru = "ru"
  ru_trans = "ru_trans"


_dot = '.'
_intonation = '!?'
_other = "():;"
_comma = ','
_special = "—"
_space = " "
_accent = '+'
_hyphen = "-"

_eos = "~"

_punctuation = _eos + _dot + _intonation + _other + _comma + _special

symbols_ = list(_punctuation + _space + _accent)

symbols_en = symbols_ + LETTERS_EN
symbols_ru = symbols_ + LETTERS_RU
symbols_ru_trans = symbols_ + LETTERS_RU_TRANS

symbols_dict = {
	Languages.en: symbols_en,
	Languages.ru: symbols_ru,
    Languages.ru_trans: symbols_ru_trans
}


def check_eos(text):
    text = text if text.endswith(_eos) else text + _eos
    return text