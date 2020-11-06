from typing import Union

from tps.modules.processor import Processor
from tps.utils import load_dict, prob2bool
from tps.symbols import punctuation, space, accent

"""
If you need to extend the Emphasizer functionality with
language-specific rules, just add a new descendant class.
"""

class Emphasizer(Processor):
    def __init__(self, dict_source: Union[str, tuple, list, dict]=None, prefer_user: bool=True):
        """
        Base emphasizer with common functionality for all languages.

        :param dict_source: Union[str, tuple, list, dict]
            Source of dictionary that contains stress pairs such as {'hello': 'hell+o'}.
            Options:
                * str - path to file.
                    The file extension must explicitly show its format in case of json and yaml files.
                    In other cases, user must set the format himself (see below).
                * tuple, list - (path, format)
                    path - path to the dictionary file
                    format - format of the dictionary file (see tps.utils.load_dict function)
                * dict - just a dict
        :param prefer_user: bool
            If true, words with stress tokens set by user will be passed as is
        """
        super().__init__()

        fmt = None
        if isinstance(dict_source, (tuple, list)):
            dict_source, fmt = dict_source

        self.entries = load_dict(dict_source, fmt)
        self.prefer_user = prefer_user


    def apply(self, string: str, **kwargs) -> str:
        """
        Splits passed string to tokens and convert each to stressed one if it presents in dictionary.
        Keep it mind, that tokenization is simple here and it's better to pass normalized string.

        :param string: str
            Your text.
        :param kwargs:
            * mask_stress: Union[bool, float]
                Whether to mask each token.
                If float, then masking probability will be computed for each token independently.
        :return: str
        """
        mask = kwargs.get("mask_stress", False)

        tokens = self.split_to_tokens(string)

        for idx, token in enumerate(tokens):
            token = self._apply_to_token(token, mask)
            tokens[idx] = token

        return self.join_tokens(tokens)


    def _apply_to_token(self, token, mask):
        if prob2bool(mask) or token in punctuation + space:
            return token

        stress_exists = token.find(accent) != -1
        if stress_exists and self.prefer_user:
            return token

        token = self.entries.get(token, token)

        return token