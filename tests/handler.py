import os
from time import time

from tps import Handler


cfd = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(cfd, "../data")


def russian():
    handler = Handler.from_charset("ru", data_dir=data_dir, silent=True)
    text = "В чащах юга жил бы цитрус? Да, но фальшивый экземпляр! " \
           "Ежик испытвал стресс, потому что под елкой не было грибочка. " \
           "Но детектив нашел его для ежика. Это столило ежику триста руб. " \
           "Синтез речи     -    это     увлекательно."
    target = "в ч+ащах +юга ж+ил бы ц+итрус? да, но фальш+ивый экземпл+яр! " \
             "+ёжик испытвал стр+эсс, потому чт+о п+од +ёлкой не было гриб+очка. " \
             "но дэтэкт+ив наш+ёл ег+о дл+я +ёжика. +это столило +ёжику тр+иста рубл+ей. " \
             "с+интэз р+ечи — +это увлек+ательно."

    user_dict = {"руб": "рублей"}

    result = handler.process_text(text, cleaners="light_punctuation_cleaners", user_dict=user_dict, keep_delimiters=False)
    assert result == target

    vector = handler.text2vec(result)
    assert handler.vec2text(vector) == result

    n = 100
    t1 = time()
    for _ in range(n):
        result = handler.process_text(text, cleaners="light_punctuation_cleaners", user_dict=user_dict, keep_delimiters=False)
        vector = handler.text2vec(result)
        handler.vec2text(vector)

    print("Handler processing time (text length is {} symbols): {}".format(len(text), (time() - t1) / n))


def english():
    handler = Handler("en")
    text = "Peter Piper picked a peck of pickled peppers;      A peck of pickled peppers Peter Piper picked"
    target = "peter piper picked a peck of pickled peppers; a peck of pickled peppers peter piper picked"

    result = handler.process_text(text, cleaners="light_punctuation_cleaners", keep_delimiters=False)

    assert result == target


def test():
    russian()
    english()


if __name__ == "__main__":
    test()