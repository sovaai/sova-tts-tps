""" from https://github.com/keithito/tacotron """

import re

from tps.phonetizers.dictionaries.base import Dict
from tps.symbols.english import _valid_symbol_set


class EnDict(Dict):
	'''Thin wrapper around CMUDict data. http://www.speech.cs.cmu.edu/cgi-bin/cmudict'''
	def __init__(self, filepath, keep_ambiguous=True):
		super().__init__(filepath)

		if not keep_ambiguous:
			self._entries = {word: pron for word, pron in self._entries.items() if len(pron) == 1}

		self._entries = {word.lower(): pron for word, pron in self._entries.items()}


	@staticmethod
	def _load_dict(filepath):
		with open(filepath, encoding='latin-1') as f:
			entries = _parse_cmudict(f)

		return entries


	def convert_word(self, word):
		return self._entries.get(word)


	def convert_text(self, text):
		#TODO: релизовать метод аналогичный русскому словарю
		return list(text)


_alt_re = re.compile(r'\([0-9]+\)')


def _parse_cmudict(file):
	cmudict = {}
	for line in file:
		if len(line) and (line[0] >= 'A' and line[0] <= 'Z' or line[0] == "'"):
			parts = line.split('  ')
			word = re.sub(_alt_re, '', parts[0])
			pronunciation = _get_pronunciation(parts[1])
			if pronunciation:
				if word in cmudict:
					cmudict[word].append(pronunciation)
				else:
					cmudict[word] = [pronunciation]
	return cmudict


def _get_pronunciation(s):
	parts = s.strip().split(' ')
	for part in parts:
		if part not in _valid_symbol_set:
			return None
	return ' '.join(parts)
