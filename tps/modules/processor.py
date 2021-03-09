import re
from collections import OrderedDict
from typing import Union, Pattern

from nltk import sent_tokenize, word_tokenize

from tps.utils import split_to_tokens, NOT_PUNCT_DICT
from tps.types import Delimiter, Charset
from tps.symbols import separator, shields


char_map = OrderedDict({
    ". ": "eos",
    "? ": "eos",
    "! ": "eos",
    ": ": "colon",
    "; ": "semicolon",
    ", ": "comma",
    " ": "space"
})

_spaced_punctuation = re.compile(r" [{}]".format("".join([char for char in char_map if char != " "])))


class Processor:
    def __init__(self, charset: Union[Charset, str], max_unit_length: int=None):
        self.charset = Charset[charset]
        self.max_unit_length = max_unit_length

        self._punct_re = re.compile(
            "[^{}]".format(
                "".join(sorted(NOT_PUNCT_DICT[self.charset]))
            )
        )


    def __call__(self, text: Union[str, list], **kwargs) -> Union[str, list]:
        return self.apply_to_text(text, **kwargs)


    def apply(self, string: str, **kwargs) -> str:
        raise NotImplementedError


    def apply_to_text(self, text: Union[str, list], **kwargs) -> Union[str, list]:
        if isinstance(text, list):
            processed = [
                self.apply_to_sentence(part, **kwargs) if not isinstance(part, Delimiter) else part for part in text
            ]
        elif isinstance(text, str):
            processed = self.apply_to_sentence(text, **kwargs)
        else:
            raise TypeError

        return processed


    def apply_to_sentence(self, sentence: str, **kwargs) -> str:
        if self.max_unit_length is not None:
            parts = self.split_to_units(sentence, self.max_unit_length)
        else:
            parts = (sentence, )

        parts = [self.apply(part, **kwargs) for part in parts]

        return " ".join(parts)


    def _calc_weight(self, text):
        _text = text
        for symb in shields:
            _text = _text.replace(symb, "")

        _text = Processor.split_to_tokens(_text, self._punct_re)

        weight = sum(len(s.split(separator)) if separator in s else len(s) for s in _text)

        return weight


    def _distribute_parts(self, parts, delimiter):
        _delimiter = "" if delimiter == " " else delimiter.replace(" ", "")

        parts_grouped = [
            delimiter.join(parts[:len(parts) // 2]) + _delimiter,
            delimiter.join(parts[len(parts) // 2:])
        ]
        return parts_grouped


    def split_to_units(self, text: str, max_unit_length: int, keep_delimiter:  bool=False) -> list:
        if self._calc_weight(text) <= max_unit_length:
            return [text]

        for delimiter in char_map:
            found = text.find(delimiter)
            if found != -1 and found != len(text) - 1:
                break

        if found != -1:
            parts = [p.strip() for p in text.split(delimiter)]
        else:
            parts = [text[:len(text) // 2], text[len(text) // 2:]]

        _parts_grouped = self._distribute_parts(parts, delimiter)
        if keep_delimiter and len(_parts_grouped) > 1:
            _parts_grouped.insert(1, Delimiter[char_map[delimiter]])

        parts_grouped = []
        for part in _parts_grouped:
            if isinstance(part, Delimiter) or self._calc_weight(part) <= max_unit_length:
                parts_grouped.append(part)
            else:
                parts_grouped.extend(self.split_to_units(part, max_unit_length, keep_delimiter))

        return parts_grouped


    @staticmethod
    def split_to_sentences(text: str, keep_delimiters: bool=False) -> list:
        parts = sent_tokenize(text)

        if keep_delimiters:
            for i in range(1, len(parts)):
                parts.insert(i * 2 - 1, Delimiter.eos)

        return parts


    @staticmethod
    def split_to_words(text: str) -> list:
        return word_tokenize(text)


    @staticmethod
    def join_words(words: list) -> str:
        words = " ".join(words)
        words = _spaced_punctuation.sub(lambda elem: elem.group(0)[-1], words)
        return words


    @staticmethod
    def split_to_tokens(text: str, punct_re: Pattern=None) -> list:
        return split_to_tokens(text, punct_re)


    @staticmethod
    def join_tokens(tokens: list) -> str:
        return "".join(tokens)