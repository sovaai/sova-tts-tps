from typing import Union

from tps.utils import load_dict
from tps.symbols import punctuation
from tps.types import Charset
from tps.modules import Processor


class Yoficator(Processor):
    def __init__(self, charset: Union[Charset, str], dict_source: Union[str, tuple, list, dict]=None):
        """
        Simple yoficator for russian language.

        :param dict_source: Union[str, tuple, list, dict]
            Source of dictionary that contains yo pairs
            such as {'елка': 'ёлка').
            Options:
                * str - path to file.
                    The file extension must explicitly show its format in case of json and yaml files.
                    In other cases, user must set the format himself (see below).
                * tuple, list - (path, format)
                    path - path to the dictionary file
                    format - format of the dictionary file (see tps.utils.load_dict function)
                * dict - just a dict
        """
        super().__init__(charset)

        fmt = None
        if isinstance(dict_source, (tuple, list)):
            dict_source, fmt = dict_source

        self.entries = load_dict(dict_source, fmt)


    def process(self, string: str, **kwargs) -> str:
        """
        Splits passed string to tokens and convert each to yoficated one if it presents in dictionary.
        Keep it mind, that tokenization is simple here and it's better to pass normalized string.

        :param string: str
            Your text.
        :param kwargs:

        :return: str
        """
        tokens = self.split_to_tokens(string)

        for idx, token in enumerate(tokens):
            if token in punctuation:
                continue
            token = self._process_token(token)
            tokens[idx] = token

        return self.join_tokens(tokens)


    def _process_token(self, token):
        return self.entries.get(token, token)