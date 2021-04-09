import os

from tps import modules as md
from tps.content import ops


cfd = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(cfd, "../data")


def processor():
    text = "В чащах юга жил бы цитрус? Да, но фальшивый экземпляр!"
    module = md.Processor()

    assert module.split_to_tokens(text) == [
        'В', ' ', 'чащах', ' ', 'юга', ' ', 'жил', ' ', 'бы', ' ', 'цитрус', '?',
        ' ',
        'Да', ',', ' ', 'но', ' ', 'фальшивый', ' ', 'экземпляр', '!'
    ]
    assert module.split_to_units(text, 15) == [
        'В чащах юга',
        'жил бы цитрус?',
        'Да,',
        'но',
        'фальшивый',
        'экземпляр!'
    ]
    assert len(module.split_to_sentences(text, keep_delimiters=True)) == 3


def check_replacer_module(module_obj, module_dict, text, target):
    try:
        module_dict = ops.find(module_dict, data_dir=data_dir, raise_exception=True)
    except FileNotFoundError:
        module_dict = ops.download(module_dict, destination=data_dir)

    module = module_obj([module_dict, "plane"])

    assert module(text) == target


def russian():
    checklist = [
        (
            md.Emphasizer,
            "stress.dict",
            "съешь же ещё этих мягких французских булок да выпей чаю.",
            "съ+ешь же ещё +этих м+ягких франц+узских б+улок да в+ыпей чаю."
        ),
        (
            md.Replacer,
            "e.dict",
            "синтез речи - это стресс",
            "с+интэз речи - это стр+эсс"
        ),
        (
            md.Replacer,
            "yo.dict",
            "ежик под елкой нашел грибочек",
            "ёжик под ёлкой нашёл грибочек"
        )
    ]

    for module_obj, module_dict, text, target in checklist:
        check_replacer_module(module_obj, module_dict, text, target)


def test():
    processor()
    russian()


if __name__ == "__main__":
    test()
