"""
Based on https://github.com/keithito/tacotron
"""
import re

from tps.utils import cleaners
from tps.symbols import symbols_dict, Languages, check_eos
from tps.phonetizers import EnDict, RuDict, RuTransDict

# Regular expression matching text enclosed in curly braces:
_curly_re = re.compile(r'(.*?)\{(.+?)\}(.*)')


cleaners_dict = {
    Languages.en: ["english_cleaners"],
    Languages.ru: ["basic_cleaners"],
    Languages.ru_trans: ["basic_cleaners"]
}


converters_dict = {
    Languages.en: EnDict,
    Languages.ru: RuDict,
    Languages.ru_trans: RuTransDict
}


class Handler:
    def __init__(self, language, dictpath=None):
        self.language = Languages[language]
        self.symbols = symbols_dict[language]

        # Mappings from symbol to numeric ID and vice versa:
        self._symbol_to_id = {s: i for i, s in enumerate(self.symbols)}
        self._id_to_symbol = {i: s for i, s in enumerate(self.symbols)}

        self.converter = converters_dict[self.language](dictpath)


    def convert_text(self, text, cleaner_names=None,stress=False, phonemes=False, dict_prime=False, stress_always=True):
        cleaned = self._clean_text(text, cleaner_names)
        converted = self.converter.convert_text(cleaned, stress, phonemes, dict_prime, stress_always)
        return converted


    def text_to_sequence(self, text, cleaner_names=None, stress=False, phonemes=False, dict_prime=True,
                         stress_always=True):
        '''Converts a string of text to a sequence of IDs corresponding to the symbols in the text.

          The text can optionally have ARPAbet sequences enclosed in curly braces embedded
          in it. For example, "Turn left on {HH AW1 S S T AH0 N} Street."

          Args:
            text: string to convert to a sequence
            language:

          Returns:
            List of integers corresponding to the symbols in the text
        '''

        text = check_eos(text)

        sequence = []
        # Check for curly braces and treat their contents as ARPAbet:
        while len(text):
            m = _curly_re.match(text)
            if not m:
                sequence += self.convert_text(text, cleaner_names, stress, phonemes, dict_prime, stress_always)
                break

            cur_text, curly, text = m.group(1), m.group(2), m.group(3)
            sequence += self.convert_text(cur_text, cleaner_names, stress, phonemes, dict_prime, stress_always)
            sequence += self.converter.convert_curly_case(curly) # TODO: проверить работу функции

        sequence = self._symbols_to_sequence(sequence)

        return sequence


    def sequence_to_text(self, sequence):
        '''Converts a sequence of IDs back to a string'''
        result = ''
        for symbol_id in sequence:
            if symbol_id in self._id_to_symbol:
                s = self._id_to_symbol[symbol_id]
                # Enclose ARPAbet back in curly braces:
                if len(s) > 1 and s[0] == '@':
                    s = '{%s}' % s[1:]
                result += s
        return result.replace('}{', ' ')


    def _clean_text(self, text, cleaner_names):
        if cleaner_names is None:
            cleaner_names = cleaners_dict[self.language]

        for name in cleaner_names:
            cleaner = getattr(cleaners, name)
            if not cleaner:
                raise Exception('Unknown cleaner: %s' % name)
            text = cleaner(text)

        return text


    def _symbols_to_sequence(self, symbs):
        return [self._symbol_to_id[s] for s in symbs if self._should_keep_symbol(s)]


    def _should_keep_symbol(self, s):
        return s in self._symbol_to_id


def get_symbols_length(language):
    language = Languages[language]
    return len(symbols_dict[language])