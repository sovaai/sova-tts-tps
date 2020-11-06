from tps.symbols.english import EN_CMU_SET, EN_SET, GRAPHEMES_EN, PHONEMES_EN_CMU
from tps.symbols.russian import RU_SET, RU_TRANS_SET, GRAPHEMES_RU, PHONEMES_RU_TRANS
from tps.types import Charset

PHONEMES = set(PHONEMES_EN_CMU + PHONEMES_RU_TRANS)

dot = '.'
intonation = '!?'
other = "():;"
comma = ','
dash = "—"
space = " "
accent = '+'
hyphen = "-"

separator = "_"
shields = ["{", "}"]

pad = "<pad>"
eos = "~"

punctuation = dot + intonation + other + comma + dash

symbols_ = [pad] + [eos] + list(punctuation + hyphen + space + accent)

symbols_en = symbols_ + EN_SET
symbols_en_cmu = symbols_ + EN_CMU_SET
symbols_ru = symbols_ + RU_SET
symbols_ru_trans = symbols_ + RU_TRANS_SET

symbols_dict = {
	Charset.en: symbols_en,
    Charset.en_cmu: symbols_en_cmu,
	Charset.ru: symbols_ru,
    Charset.ru_trans: symbols_ru_trans
}