import os

from tps import symbols
from tps.utils import prob2bool
from tps.symbols import russian as ru_trans_symbs
from tps.phonetizers.dictionaries.base import Dict


class RuDict(Dict):
    def __init__(self, filepath=None):
        super().__init__(filepath)


    def convert_word(self, word):
        return list(word)


    def convert_text(self, text):
        return list(text)


class RuTransDict(Dict):
    def __init__(self, filepath=None):
        if filepath is not None:
            assert os.path.exists(filepath)

        super().__init__(filepath)


    def convert_text(self, text, stress=False, phonemes=False, dict_prime=True, stress_always=True):
        text = self._prepare_punctuation(text)
        converted = []

        for i, word in enumerate(text):
            if word in symbols._punctuation + symbols._space:
                word = [word]
            else:
                try:
                    new_word = self.convert_word(word, stress, phonemes, dict_prime, stress_always)
                    word = new_word.split(" ")
                except Exception:
                    print("Some problems with converting {} word in {} sentence".format(word, text))
                    word = convert(word).split(" ")

            converted.extend(word)

        if converted[-1] == " ":
            converted.pop()

        return converted


    def convert_word(self, item, stress=False, phonemes=False, dict_prime=True, stress_always=True):
        phonemes = prob2bool(phonemes) if isinstance(phonemes, (int, float)) else phonemes
        stress = prob2bool(stress) if isinstance(stress, (int, float)) else stress

        stress_exists = item.find(symbols._accent) != -1

        key = item.replace(symbols._accent, "")

        word = convert(item) if stress else convert(key)
        dict_word = self._get_from_dict(key, word, stress_exists, stress, phonemes, dict_prime)

        get_dict_word = phonemes or (dict_prime and stress) or (not stress_exists and stress_always)
        word = dict_word if get_dict_word else word

        word = extract_stress(word)

        return word


    def convert_curly_case(self, text):
        return text.split(" ")


    def _get_from_dict(self, key, word, stress_exists, stress, phonemes, dict_prime):
        value = self._entries.get(key, None)
        dict_word = word
        if value is not None:
            if phonemes:
                dict_word = value.get("phoneme")
                dict_word = dict_word if dict_word is not None else word

                unstressed = dict_word.replace("1", "")

                if stress:
                    if not dict_prime and stress_exists:
                        mask = make_stress_mask(word)
                        dict_word = put_vowel_mask(unstressed, mask)
                        dict_word = stick_stress(dict_word)
                else:
                    dict_word = unstressed
            elif stress:
                dict_word = value.get("stress")
                dict_word = dict_word if dict_word is not None else word

        return dict_word


    @staticmethod
    def _prepare_punctuation(text):
        prepared = ""
        for s in text:
            prepared += "*" + s + "*" if s in symbols._punctuation + symbols._space else s

        prepared = prepared.split("*")
        prepared = [t for t in prepared if t != ""]

        return prepared


    @staticmethod
    def _load_dict(filepath):
        with open(filepath, "r", encoding="utf-8") as ouf:
            lines = ouf.readlines()

        lines = [line.strip().split("|") for line in lines]

        entries = {
            line[0]: {
                "phoneme": line[1] if line[1] else None,
                "stress": line[2] if line[2] else None
            } for line in lines
        }

        return entries


def make_stress_mask(word):
    word = word.split(" ") if not isinstance(word, list) else word
    mask = []

    for phoneme in word:
        if phoneme in ru_trans_symbs.vowels.values():
            mask.append(False)
        elif phoneme in ru_trans_symbs.stressed_vowels:
            mask.append(True)

    return mask


def put_vowel_mask(word, mask):
    word = word.split(" ") if not isinstance(word, list) else word
    i = 0
    for j, letter in enumerate(word):
        if letter in ru_trans_symbs.vowels.values() or letter == ru_trans_symbs.o_unstressed:
            if mask[i]:
                word.insert(j, "+")
                break
            i += 1

    return word


def extract_stress(word):
    word = word.split(" ") if not isinstance(word, list) else word
    word = [s if "1" not in s else "{} {}".format(symbols._accent, s.replace("1", "")) for s in word]

    return " ".join(word)


def stick_stress(word):
    word = word.split(" ") if not isinstance(word, list) else word

    idx = word.index(symbols._accent)
    word[idx + 1] = word[idx + 1] + "1"
    word.remove(symbols._accent)

    return " ".join(word)


def pallatize(phones):
    converted = []

    for i, phone in enumerate(phones[:-1]):
        if i == 0:
            continue

        new_phone = phone

        if phone[0] in ru_trans_symbs.hard_cons:
            if phones[i + 1][0] in ru_trans_symbs.softletters:
                new_phone = (ru_trans_symbs.hard_cons[phone[0]] + "j", 0)
            else:
                new_phone = (ru_trans_symbs.hard_cons[phone[0]], 0)
        elif phone[0] in ru_trans_symbs.other_cons:
            new_phone = (ru_trans_symbs.other_cons[phone[0]], 0)

        converted.append(new_phone)

    return converted


def convert_vowels(phones):
    jphones = set("яюеё")

    new_phones = []
    prev = ""
    for phone in phones:
        if not prev or prev in ru_trans_symbs.startsyl:
            if phone[0] in jphones:
                new_phones.append("j")
        if phone[0] in ru_trans_symbs.vowels:
            if phone[1] == 1:
                new_phones.append(ru_trans_symbs.vowels[phone[0]] + str(phone[1]))
            else:
                new_phones.append(ru_trans_symbs.vowels[phone[0]])
        else:
            new_phones.append(phone[0])
        prev = phone[0]

    return new_phones


def convert(word, extract_stress_=False):
    word = "#" + word + "#"

    # Assign stress marks
    stress_phones = []
    stress = 0
    for letter in word:
        if letter == symbols._accent:
            stress = 1
        else:
            stress_phones.append((letter, stress))
            stress = 0

    # Pallatize
    phones = pallatize(stress_phones)

    # Assign stress
    phones = convert_vowels(phones)

    # Filter
    phones = [x for x in phones if x not in ru_trans_symbs.others]
    phones = " ".join(phones)

    return extract_stress(phones) if extract_stress_ else phones
