GRAPHEMES_RU = list("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")

softletters = set("яёюиье")
startsyl = set("ъьаяоёуюэеиы-")
others = {"ь", "ъ", "#"}

hard_cons = {
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "з": "z",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "ф": "f",
    "х": "h"
}

soft_cons = [i + "j" for i in hard_cons.values()]

other_cons = {
    "ж": "zh",
    "ц": "c",
    "ч": "ch",
    "ш": "sh",
    "щ": "sch",
    "й": "j"
}

vowels = {
    "а": "a",
    "я": "a",
    "у": "u",
    "ю": "u",
    "о": "o",
    "ё": "o",
    "э": "e",
    "е": "e",
    "и": "i",
    "ы": "y",
}

stressed_vowels = [i + "1" for i in vowels.values()]

o_unstressed = "ay"

PHONEMES_RU_TRANS = sorted(set(list(hard_cons.values()) + soft_cons + list(other_cons.values()) +
                              list(vowels.values()) + [o_unstressed]))

RU_SET = GRAPHEMES_RU
RU_TRANS_SET = PHONEMES_RU_TRANS
