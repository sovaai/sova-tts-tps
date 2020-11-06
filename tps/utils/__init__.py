import os
import re
import json
import yaml
import numpy as np

from tps.types import Charset
from tps import symbols


GRAPHEME_DICT = {
    Charset.en: symbols.english.GRAPHEMES_EN,
    Charset.en_cmu: symbols.english.GRAPHEMES_EN,
    Charset.ru: symbols.russian.GRAPHEMES_RU,
    Charset.ru_trans: symbols.russian.GRAPHEMES_RU
}


def prob2bool(prob):
    return prob if isinstance(prob, bool) else np.random.choice([True, False], p=[prob, 1 - prob])


def split_to_tokens(text):
    prepared = ""
    for s in text:
        prepared += "*" + s + "*" if s in symbols.punctuation + symbols.space else s

    prepared = prepared.split("*")
    prepared = [t for t in prepared if t != ""]

    return prepared


def hide_stress(regexp, text):
    return regexp.sub(lambda elem: elem.group(0)[-1].upper(), text)


def reveal_stress(regexp, text):
    return regexp.sub(lambda elem: "+" + elem.group(0).lower(), text)


def get_stressed_letters_re(charset):
    charset = Charset[charset]
    regexp = re.compile(r"\+[{}]".format("".join(GRAPHEME_DICT[charset])))

    return regexp


def get_capital_letters_re(charset):
    charset = Charset[charset]
    regexp = re.compile("[{}]".format("".join(GRAPHEME_DICT[charset]).upper()))

    return regexp


def load_dict(dict_source, fmt=None):
    _dict = {}

    if isinstance(dict_source, str):
        _, ext = os.path.splitext(dict_source)
        if ext in [".json", ".yaml"]:
            fmt = ext.replace(".", "")
        elif fmt is None:
            raise ValueError("File format must be specified ['json', 'yaml', 'plane']")

        assert os.path.exists(dict_source)

        with open(dict_source, "r", encoding="utf-8") as stream:
            if fmt == "json":
                _dict = json.load(stream)
            elif fmt == "yaml":
                _dict = yaml.safe_load(stream)
            elif fmt == "plane":
                _dict = stream.read().splitlines()
                _dict = tuple(line.split("|") for line in _dict)
                _dict = {elem[0]: elem[1] for elem in _dict}
            else:
                raise ValueError("File format must be specified ['json', 'yaml', 'plane']")

    elif isinstance(dict_source, dict):
        _dict = dict_source
    elif dict_source is None:
        pass
    else:
        raise TypeError

    return _dict


def save_dict(dict_obj, filepath, fmt=None):
    _dict = {}

    _, ext = os.path.splitext(filepath)
    if ext in [".json", ".yaml"]:
        fmt = ext.replace(".", "")
    elif fmt is None:
        raise ValueError("File format must be specified ['json', 'yaml', 'plane']")

    with open(filepath, "w", encoding="utf-8") as stream:
        if fmt == "json":
            json.dump(dict_obj, stream, indent=2, ensure_ascii=False)
        elif fmt == "yaml":
            yaml.dump(dict_obj, stream, indent=2, allow_unicode=True)
        else:
            raise ValueError("File format must be specified ['json', 'yaml']")

    return filepath