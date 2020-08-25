from tps.phonetizers import RuTransDict
from tps.phonetizers.dictionaries.russian import stick_stress, extract_stress, convert


def test_stress_convert():
	text = "j o1 l k a"
	assert stick_stress(extract_stress(text)) == text


def test_convert_func():
	test_set = {
		"когда-то": "k o g d a t o",
		"адъюнктура": "a d j u n k t u r a",
		"безалаберный": "bj e z a l a bj e r n y j",
		"пом+ятый": "p o mj a1 t y j",
		"б+ольно": "b o1 lj n o",
		"нетаки": "nj e t a kj i",
		"ч+учело": "ch u1 ch e l o",
		"шуршащий": "sh u r sh a sch i j",
		"ж+итница": "zh i1 t nj i c a",
		"тёмно-серый": "tj o m n o sj e r y j",
		"гуверн+антка": "g u vj e r n a1 n t k a",
		"мимозы": "mj i m o z y",
		"+ёлка": "j o1 l k a",
		"бель+ё": "bj e lj j o1",
		"поели": "p o j e lj i"
	}

	for word, phones in test_set.items():
		converted = convert(word)
		assert phones == converted, "Expected {}, got {}".format(phones, converted)


def test_converter(converter: RuTransDict):
	text = "съешь ещё этих мягких (французских) булок, да выпей же чаю!!!"

	expected_stress = "sj+esh jesch+o +etjih mj+agkjih (franc+uzskjih) b+ulok, da v+ypjej zhe chaju!!!"
	expected_phonemes = "sjesh jischo etjih mjahkjih (francusskjih) bulayk, da vypjij zhe chaju!!!"
	expected_both = "sj+esh jisch+o +etjih mj+ahkjih (franc+usskjih) b+ulayk, da v+ypjij zhe chaju!!!"

	stress = "".join(converter.convert_text(text, stress=True))
	phonemes = "".join(converter.convert_text(text, phonemes=True))
	both = "".join(converter.convert_text(text, stress=True, phonemes=True))

	assert stress == expected_stress
	assert phonemes == expected_phonemes
	assert both == expected_both


def test_stress(converter: RuTransDict):
	text1 = "съешь ещё этих мягк+их — французск+их — булок, да выпей же чаю."

	expected1 = {
		"00": "sjesh jescho etjih mjagkjih — francuzskjih — bulok, da vypjej zhe chaju.",
		"01": "sjesh jescho etjih mjagkjih — francuzskjih — bulok, da vypjej zhe chaju.",
		"10": "sj+esh jesch+o +etjih mjagkj+ih — francuzskj+ih — b+ulok, da v+ypjej zhe chaju.",
		"11": "sj+esh jesch+o +etjih mj+agkjih — franc+uzskjih — b+ulok, da v+ypjej zhe chaju."
	}

	for flags, value in expected1.items():
		converted = "".join(converter.convert_text(text1, stress=bool(int(flags[0])), dict_prime=bool(int(flags[1]))))
		assert converted == value

	text2 = "кто сказал, что слоны не умеют танцевать?"

	expected2 = {
		"00": "kto skazal, chto slony nje umjejut tancevatj?",
		"01": "kto skazal, chto slony nje umjejut tancevatj?",
		"10": "kt+o skaz+al, chto slon+y nje umj+ejut tancev+atj?",
		"11": "kt+o skaz+al, chto slon+y nje umj+ejut tancev+atj?"
	}

	for flags, value in expected2.items():
		converted = "".join(converter.convert_text(text2, stress=bool(int(flags[0])), dict_prime=bool(int(flags[1]))))
		assert converted == value


def test_stress_extract(converter: RuTransDict):
	text = "кт+о сказ+ал, чт+о слон+ы н+е ум+еют танцев+ать?"

	converted = "".join(converter.convert_text(text, stress=True, dict_prime=False))
	assert converted == "kt+o skaz+al, cht+o slon+y nj+e umj+ejut tancev+atj?"


def test_phonemes(converter: RuTransDict):
	text = "съешь ещё этих мягк+их — французск+их — булок, да выпей же чаю."

	expected = {
		"000": "sjesh jescho etjih mjagkjih — francuzskjih — bulok, da vypjej zhe chaju.",
		"001": "sjesh jescho etjih mjagkjih — francuzskjih — bulok, da vypjej zhe chaju.",
		"010": "sjesh jischo etjih mjahkjih — francusskjih — bulayk, da vypjij zhe chaju.",
		"011": "sjesh jischo etjih mjahkjih — francusskjih — bulayk, da vypjij zhe chaju.",
		"100": "sj+esh jesch+o +etjih mjagkj+ih — francuzskj+ih — b+ulok, da v+ypjej zhe chaju.",
		"101": "sj+esh jesch+o +etjih mj+agkjih — franc+uzskjih — b+ulok, da v+ypjej zhe chaju.",
		"110": "sj+esh jisch+o +etjih mjahkj+ih — francusskj+ih — b+ulayk, da v+ypjij zhe chaju.",
		"111": "sj+esh jisch+o +etjih mj+ahkjih — franc+usskjih — b+ulayk, da v+ypjij zhe chaju."
	}

	for flags, value in expected.items():
		converted = "".join(converter.convert_text(text, stress=bool(int(flags[0])), phonemes=bool(int(flags[1])),
		                                           dict_prime=bool(int(flags[2]))))
		assert converted == value


def test_dict(converter: RuTransDict):
	for i, key in enumerate(converter):
		print("\rChecked {} out of {} keys".format(i + 1, len(converter)), end="")

		converter.convert_word(key, stress=True)
		converter.convert_word(key, phonemes=True)


if __name__ == "__main__":
	converter = RuTransDict(filepath="../data/ru_trans.dic")

	test_stress_convert()
	test_convert_func()
	test_converter(converter)
	test_stress(converter)
	test_stress_extract(converter)
	test_phonemes(converter)
	test_dict(converter)
