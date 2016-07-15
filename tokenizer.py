import re
import pymorphy2
import collections


cool_tuple = collections.namedtuple('CoolTuple', ('word', 'type', 'tag', 'normal_form', 'score'))


class Tokenizer:
    #
    #
    #

    whitespace = set('“”\n\t _/')

    token_type = {'.': 'point',
                  ',': 'comma',
                  ';': 'semicolon',
                  ':': 'colon',
                  '№': 'num',
                  '(': 'open_bracket',
                  ')': 'close_bracket',
                  '%': 'percent'}

    alphabet = set('ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁйцукенгшщзхъфывапролджэячсмитьбюё')
    digits = set('1234567890')

    morph = pymorphy2.MorphAnalyzer()

    @staticmethod
    def append_token(lst, elem, type_):
        t = Tokenizer.morph.parse(elem)[0]
        lst.append(cool_tuple(elem, type_, t.tag, t.normal_form, t.score))

    @staticmethod
    def get_tokens(text, debug=False):
        #  Делит текст на токены, определяет нормальную форму,
        #  а также часть речи, род, падеж, число
        #

        tokens = []
        state = 0
        token = ''
        for index, value in enumerate(text):
            if state == 0:
                if token != '' and token not in Tokenizer.whitespace:
                    if token in Tokenizer.token_type:
                        Tokenizer.append_token(tokens, token, Tokenizer.token_type[token])

                    else:
                        Tokenizer.append_token(tokens, token, 'Unk')

                token = value
                if value in Tokenizer.alphabet:
                    state = 1

                elif value in Tokenizer.digits:
                    state = 3

            elif state == 1:  # Очередная буква в слове
                if value in Tokenizer.alphabet:
                    token += value

                elif value == '-':
                    token += value
                    state = 2

                else:
                    Tokenizer.append_token(tokens, token, 'word')
                    token = value
                    state = 0

            elif state == 2:  # Очередная буква после дефиса
                if value in Tokenizer.alphabet:
                    token += value

                else:
                    Tokenizer.append_token(tokens, token, 'word')
                    token = value
                    state = 0

            elif state == 3:  # Очередная цифра
                if value in Tokenizer.digits:
                    token += value

                elif value == '.':
                    token += value
                    state = 4

                else:
                    Tokenizer.append_token(tokens, token, 'number')
                    token = value
                    state = 0

            elif state == 4:  # Очередная цифра после точки
                if value in Tokenizer.digits:
                    token += value

                else:
                    Tokenizer.append_token(tokens, token, 'number')
                    token = value
                    state = 0

            if debug:
                print(state, token)

        Tokenizer.append_token(tokens, '#', 'end')

        return tokens
