import re
import pymorphy2
import collections


class Splitter:
    # Метод run возвращает список предложений и токенов

    HYPHEM = '-'
    POINT = '.'

    alphabet = set('ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁйцукенгшщзхъфывапролджэячсмитьбюё')
    digits = set('1234567890')
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

    morph = pymorphy2.MorphAnalyzer()
    Lexeme = collections.namedtuple('Lexeme', ('word', 'token_type', 'morph'))

    def __init__(self, debug=False):
        self.debug = debug
        self.lexeme_list = []
        self.sentence_list = []

    def run(self, text):
        self.lexeme_list = self._get_lexemes(text)
        self._post_processing(self.lexeme_list)

        return self.lexeme_list

    @staticmethod
    def _get_lexemes(text, debug=False):
        #  Делит текст на лексемы, определяет тип токена, нормальную форму,
        #  а также часть речи, род, падеж, число

        def add(lst, elem, type_):
            t = Splitter.morph.parse(elem)
            lst.append(Splitter.Lexeme(elem, type_, t))

        lexeme_list = []
        state = 0
        lexeme = ''
        for index, value in enumerate(text):
            if state == 0:
                if lexeme != '' and lexeme not in Splitter.whitespace:
                    if lexeme in Splitter.token_type:
                        add(lexeme_list, lexeme, Splitter.token_type[lexeme])
                    else:
                        add(lexeme_list, lexeme, 'Unk')

                lexeme = value
                if value in Splitter.alphabet:
                    state = 1
                elif value in Splitter.digits:
                    state = 3

            elif state == 1:  # Очередная буква в слове
                if value in Splitter.alphabet:
                    lexeme += value
                elif value == Splitter.HYPHEM:
                    lexeme += value
                    state = 2
                else:
                    add(lexeme_list, lexeme, 'word')
                    lexeme = value
                    state = 0

            elif state == 2:  # Очередная буква после дефиса
                if value in Splitter.alphabet:
                    lexeme += value
                else:
                    add(lexeme_list, lexeme, 'word')
                    lexeme = value
                    state = 0

            elif state == 3:
                if value in Splitter.digits:
                    lexeme += value
                elif value == Splitter.POINT:
                    lexeme += value
                    state = 4
                else:
                    add(lexeme_list, lexeme, 'int')
                    lexeme = value
                    state = 0

            elif state == 4:
                if value in Splitter.digits:
                    lexeme += value
                    state = 5
                elif value == Splitter.POINT:
                    lexeme += value
                else:
                    add(lexeme_list, lexeme, 'par')
                    lexeme = value
                    state = 0

            elif state == 5:
                if value in Splitter.digits:
                    lexeme += value
                elif value == Splitter.POINT:
                    lexeme += value
                    state = 4
                else:
                    add(lexeme_list, lexeme, 'float')
                    lexeme = value
                    state = 0

            if debug:
                print(state, lexeme)

        add(lexeme_list, '#', 'end')
        return lexeme_list

    @staticmethod
    def _post_processing(lexeme_list):
        # Убираем лишние _ нижние подчеркивания

        trigger = False
        index = 0
        value = lexeme_list[index].word
        while value != '#':
            if value == '_':
                if not trigger:
                    trigger = True
                    index += 1
                else:
                    del lexeme_list[index]

            else:
                trigger = False
                index += 1

            value = lexeme_list[index].word

    @staticmethod
    def _get_sentences(lexeme_list):
        # Делим список токенов на предложения

        sentence_list = []
        #for t in lexeme_list:
        #    pass

        return sentence_list





