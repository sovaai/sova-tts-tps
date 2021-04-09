# Text processing for speech synthesis

This package was created in order to construct, on a modular basis, the text processors necessary to obtain a text prepared for submission to speech synthesis systems. At the moment, only Russian and English languages are supported. There is only basic support for English (see [Basic functionality](https://github.com/sovaai/sova-tts/wiki/NLP-preprocessor#basic-functionality)); following modules modules are implemented for Russian:

* Е-to-Э replacement module based on [dictionary](http://dataset.sova.ai/SOVA-TTS/tps_data/e.dict)
* Е-to-Ё replacement module based on [dictionary](http://dataset.sova.ai/SOVA-TTS/tps_data/yo.dict)
* Stress setting module based on [dictionary](http://dataset.sova.ai/SOVA-TTS/tps_data/stress.dict)

The project has the potential for expansion with other modules (g2p, normalizer) and languages.

# How to use

## Modules
Let us say you need to stress words in some text. You need stress setting module (Emphasizer) to complete this task:
```python
from tps import download
from tps.data import find
from tps.modules import Emphasizer


try:
    stress_dict = find("stress.dict", raise_exception=True)
except FileNotFoundError:
    stress_dict = download("stress.dict")

emphasizer = Emphasizer("ru", (stress_dict, "plane"))
text = "Привет, мир! Смотри, как я умею ставить ударения в словах."
emphasizer.process_text(text)
```
results in
```
'Привет, м+ир! Смотри, как я ум+ею ставить удар+ения в слов+ах.'
```

Since this module is case sensitive, you get a different result if you lowercase the text:

```python
emphasizer.process_text(text.lower())
```
results in
```
'прив+ет, м+ир! смотри, как я ум+ею ставить удар+ения в слов+ах.'
```
## Handler

Let us say you need to prepare a text for transfer to the speech synthesis system. There are two possible scenarios for you.

### Basic functionality
Let us say you already have a cleaned up and marked up text for training synthesis system. In this case, you only need the basic functionality of the Handler class, such as: 
* storing a fixed symbolic dictionary
* conversion to lower case
* obtaining vectors of sentences based on a symbolic dictionary
* getting suggestions from vectors
* some additional cleaning

In that case the following code is enough
```python
from tps import Handler

handler = Handler("ru")
text = "В чащах юга жил бы цитрус? Да, но фальшивый экземпляр!"

result = handler.process_text(text, keep_delimiters=False)
print(result)
```
```
'в чащах юга жил бы цитрус? да, но фальшивый экземпляр!'
```
```python
vector = handler.text2vec(result)
print(vector)
```
```
[16, 12, 38, 14, 40, 14, 36, 12, 45, 17, 14, 12, 21, 23, 26, 12, 15, 42, 12, 37, 23, 33, 31, 34, 32, 4, 12, 18, 14, 9, 12, 28, 29, 12, 35, 14, 26, 43, 39, 23, 16, 42, 24, 12, 44, 25, 22, 19, 27, 30, 26, 46, 31, 3]
```

### Connecting modules
In case you need to prepare text for inference, you may need to connect various modules that improve the text sent for synthesis. For Russian language just use `from_charset` method of Handler class (`silent=True` allows loading in automatic mode the data required for the modules to work):

```python
from tps import Handler

handler = Handler.from_charset("ru", silent=True)
text = "В чащах юга жил бы цитрус? Да, но фальшивый экземпляр!"

result = handler.process_text(text, keep_delimiters=False)
print(result)
```
```
в ч+ащах +юга ж+ил бы ц+итрус? да, но фальш+ивый экземпл+яр!
```

or, if you need to preserve delimiters:

```python
result = handler.process_text(text, keep_delimiters=True)
print(result)
```
```
['в ч+ащах +юга ж+ил бы ц+итрус?', <Pause.eos: 500ms>, 'да, но фальш+ивый экземпл+яр!']
```
also there is possibility to pass the user dictionary and necessary cleaner functions (including custom ones)

```python
text = "TTS     -    это     увлекательно."
user_dict = {"tts": "синтез речи"}

result = handler.process_text(text, cleaners="light_punctuation_cleaners", user_dict=user_dict, keep_delimiters=False)
```
```
'с+интэз р+ечи — +это увлек+ательно.'
```

In case you want to link your other modules with the handler, then do this when initializing the class instance

```python
handler = Handler("ru", modules=some_modules_list)
```

# How to add new module
The most important thing when creating a new module is to remember that it must inherit from the [Processor](https://github.com/sovaai/sova-tts-tps/blob/master/tps/modules/processor.py) class in order to have a consistent interface with other modules.

# How to add new language
The key folder when adding a new language or a new character set is folder [symbols](https://github.com/sovaai/sova-tts-tps/tree/master/tps/symbols). If you add a new language, create a file with the name of the language inside, and then do it by analogy with the existing languages.
