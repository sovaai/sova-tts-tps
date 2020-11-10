import re
from typing import Union

from tps.modules.phonetizer.rule_based.independent import Phonetizer
from tps.utils import prob2bool
from tps.symbols import punctuation, space, accent, separator, shields, russian, symbols_dict
from tps.types import Charset


class RUglyPhonetizer(Phonetizer):
    def __init__(self, dict_source: Union[str, tuple, list, dict]=None):
        super().__init__(dict_source)

        self.charset = Charset.ru_trans
        self._symbols = symbols_dict[self.charset]


    def _apply_to_token(self, token, mask):
        if token in punctuation + space:
            return token

        ugly_token = convert(token)

        if len(ugly_token) == 1 and ugly_token not in self._symbols:
            return ugly_token

        if prob2bool(mask):
            return shields[0] + ugly_token + shields[1]

        stress_exists = token.find(accent) != -1
        if not stress_exists:  # we won't phonetize words without stress, that's all
            return shields[0] + ugly_token + shields[1]

        token = self.entries.get(token, ugly_token)

        return shields[0] + token + shields[1]


_stressed_vowels = re.compile(r"[{}]1".format("".join(russian.vowels)))

def extract_stress(word):
    return _stressed_vowels.sub(lambda elem: accent + separator + elem.group(0)[0], word)


def pallatize(phones):
    converted = []

    for i, phone in enumerate(phones[:-1]):
        if i == 0:
            continue

        new_phone = phone

        if phone[0] in russian.hard_cons:
            if phones[i + 1][0] in russian.softletters:
                new_phone = (russian.hard_cons[phone[0]] + "j", 0)
            else:
                new_phone = (russian.hard_cons[phone[0]], 0)
        elif phone[0] in russian.other_cons:
            new_phone = (russian.other_cons[phone[0]], 0)

        converted.append(new_phone)

    return converted


def convert_vowels(phones):
    jphones = set("яюеё")

    new_phones = []
    prev = ""
    for phone in phones:
        if not prev or prev in russian.startsyl:
            if phone[0] in jphones:
                new_phones.append("j")
        if phone[0] in russian.vowels:
            if phone[1] == 1:
                new_phones.append(accent + separator + russian.vowels[phone[0]])
            else:
                new_phones.append(russian.vowels[phone[0]])
        else:
            new_phones.append(phone[0])
        prev = phone[0]

    return new_phones


def convert(word):
    word = "#" + word + "#"

    # Assign stress marks
    stress_phones = []
    stress = 0
    for letter in word:
        if letter == accent:
            stress = 1
        else:
            stress_phones.append((letter, stress))
            stress = 0

    # Pallatize
    phones = pallatize(stress_phones)

    # Assign stress
    phones = convert_vowels(phones)

    # Filter
    phones = [x for x in phones if x not in russian.others]
    phones = separator.join(phones)

    return phones