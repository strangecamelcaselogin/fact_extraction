import re
import pymorphy2
import collections


cool_tuple = collections.namedtuple('CoolTuple', ('word', 'type', 'tag', 'normal_form', 'score'))


class Splitter:
    #
    #
    #
    HYPHEM = '-'
    POINT = '.'
    whitespace = set('\n\t/ ')

    token_type = {'.': 'point',
                  ',': 'comma',
                  ';': 'semicolon',
                  ':': 'colon',
                  '№': 'num',
                  '(': 'open_bracket',
                  ')': 'close_bracket',
                  '%': 'percent',
                  '_': 'field',
                  '"': 'quote',
                  "'": 'sing_quote',
                  '“': 'ru_quote_open',
                  '”': 'ru_quote_close'}

    alphabet = set('ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁйцукенгшщзхъфывапролджэячсмитьбюё')
    digits = set('1234567890')

    morph = pymorphy2.MorphAnalyzer()

    @staticmethod
    def append_token(lst, elem, type_):
        t = Splitter.morph.parse(elem)[0]
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
                if token != '' and token not in Splitter.whitespace:
                    if token in Splitter.token_type:
                        Splitter.append_token(tokens, token, Splitter.token_type[token])
                    else:
                        Splitter.append_token(tokens, token, 'Unk')

                token = value
                if value in Splitter.alphabet:
                    state = 1
                elif value in Splitter.digits:
                    state = 3

            elif state == 1:  # Очередная буква в слове
                if value in Splitter.alphabet:
                    token += value
                elif value == Splitter.HYPHEM:
                    token += value
                    state = 2
                else:
                    Splitter.append_token(tokens, token, 'word')
                    token = value
                    state = 0

            elif state == 2:  # Очередная буква после дефиса
                if value in Splitter.alphabet:
                    token += value
                else:
                    Splitter.append_token(tokens, token, 'word')
                    token = value
                    state = 0

            elif state == 3:
                if value in Splitter.digits:
                    token += value
                elif value == Splitter.POINT:
                    token += value
                    state = 4
                else:
                    Splitter.append_token(tokens, token, 'int')
                    token = value
                    state = 0

            elif state == 4:
                if value in Splitter.digits:
                    token += value
                    state = 5
                elif value == Splitter.POINT:
                    token += value
                else:
                    Splitter.append_token(tokens, token, 'par')
                    token = value
                    state = 0

            elif state == 5:
                if value in Splitter.digits:
                    token += value
                elif value == Splitter.POINT:
                    token += value
                    state = 4
                else:
                    Splitter.append_token(tokens, token, 'float')
                    token = value
                    state = 0

            if debug:
                print(state, token)

        Splitter.append_token(tokens, '#', 'end')

        return tokens

    @staticmethod
    def post_processing(token_list):
        # Убираем лишние _ нишние подчеркивания

        trigger = False
        index = 0
        value = token_list[index].word
        while value != '#':
            if value == '_':
                if not trigger:
                    trigger = True
                    index += 1
                else:
                    del token_list[index]

            else:
                trigger = False
                index += 1

            value = token_list[index].word





