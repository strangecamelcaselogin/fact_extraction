import re


class Tokenizer:
    whitespace = set('()“”\n\t,.;: _/')
    alphabet = set('ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁйцукенгшщзхъфывапролджэячсмитьбюё№')
    digits = set('1234567890')

    @staticmethod
    def get_words(text):
        # Получаем лексемы без пробелов, запятых, точек
        # Кривой способ, пусть будет

        words = []
        word = ''
        while text != '':
            v = text[0]
            if v in Tokenizer.whitespace:
                if word != '':
                    words.append(word)
                    word = ''

            else:
                word += v

            text = text[1:]

        if word != '':
            words.append(word)

        return words

    @staticmethod
    def get_words2(text, debug=False):
        # Получаем лексемы без пробелов, запятых, точек

        words = []
        state = 0
        word = ''
        for i, v in enumerate(text):
            if state == 0:
                if word != '':
                    words.append(word)
                    word = ''

                if v in Tokenizer.alphabet:
                    state = 1
                    word = v

                elif v in Tokenizer.digits:
                    state = 2
                    word = v

            elif state == 1:
                if v in Tokenizer.alphabet:
                    word += v

                elif v in Tokenizer.whitespace:
                    state = 0

            elif state == 2:
                if v in Tokenizer.digits or v == '.':
                    word += v

                elif v in Tokenizer.whitespace:
                    state = 0

            if debug:
                print('{} - {} === {}'.format(i, v, state))

        return words

    @staticmethod
    def tokens(text):
        pass
