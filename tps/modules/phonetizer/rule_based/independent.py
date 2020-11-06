from typing import Union

from tps.modules.processor import Processor
from tps.utils import load_dict, prob2bool
from tps.symbols import punctuation, space, accent, shields, separator

"""
If you need to extend the Phonetizer functionality with
language-specific rules, just add a new descendant class.
"""

class Phonetizer(Processor):
    def __init__(self, dict_source: Union[str, tuple, list, dict]=None):
        """
        Base phonetizer with common functionality for all languages.

        :param dict_source: Union[str, tuple, list, dict]
            Source of dictionary that contains phonetization pairs such as (hello, HH AH L OW) in the case of CMU dict.
            Options:
                * str - path to file.
                    The file extension must explicitly show its format in case of json and yaml files.
                    In other cases, user must set the format himself (see below).
                * tuple, list - (path, format)
                    path - path to the dictionary file
                    format - format of the dictionary file (see tps.utils.load_dict function)
                * dict - just a dict
        """
        super().__init__()

        fmt = None
        if isinstance(dict_source, (tuple, list)):
            dict_source, fmt = dict_source

        self.entries = load_dict(dict_source, fmt)


    def apply(self, string: str, **kwargs) -> str:
        """
        Splits passed string to tokens and convert each to stressed one if it presents in dictionary.
        Keep it mind, that tokenization is simple here and it's better to pass normalized string.

        :param string: str
            Your text.
        :param kwargs:
            * mask_phonemes: Union[bool, float]
                Whether to mask each token.
                If float, then masking probability will be computed for each token independently.
        :return: str
        """
        mask = kwargs.get("mask_phonemes", False)

        tokens = self.split_to_tokens(string)

        for idx, token in enumerate(tokens):
            token = self._apply_to_token(token, mask)
            tokens[idx] = token

        return self.join_tokens(tokens)


    def _apply_to_token(self, token, mask):
        if prob2bool(mask) or token in punctuation + space:
            return token

        stress_exists = token.find(accent) != -1
        if not stress_exists: # we won't phonetize words without stress, that's all
            return token

        token = self.entries.get(token, token) # word -> W_O_R_D

        return shields[0] + token + shields[1] # W_O_R_D -> {W_O_R_D}