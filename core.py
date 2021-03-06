from time import time
from datetime import datetime
from prettytable import PrettyTable

from splitter import Splitter


class Core:
    def __init__(self):
        pass

    @staticmethod
    def load_text(filename):
        with open(filename, 'r') as f:
            text = f.read()

        return text

    @staticmethod
    def report(data):
        rt = datetime.fromtimestamp(time())
        filename = '{}.{}_{}.{}.txt'.format(rt.day, rt.month, rt.hour, rt.minute)
        with open(filename, 'w') as f:
            for d in data:
                print(d, file=f)

        print('Файл отчет успешно создан')

    def extract_terms(self, lexeme_list, count=0, debug=False):
        # Считаем количество использований каждой лексемы в тексте
        term_list = dict()
        for lex in lexeme_list:
            ftag = lex.morph[0].tag
            fn_form = lex.morph[0].normal_form
            if lex.token_type == 'word' and 'NOUN' in ftag:
                if fn_form in term_list:
                    term_list[fn_form] += 1
                else:
                    term_list[fn_form] = 1

            if debug:
                print('{} {}:: {}'.format(lex, (25 - len(lex)) * ' ', ftag))

        term_list = list(reversed(sorted(term_list.items(), key=lambda x: x[1])))

        return term_list if count == 0 else term_list[:count]

    def run(self, filename):
        splt = Splitter()

        lexemes, _ = splt.run(self.load_text(filename))
        print(*[lex.word for lex in lexemes])

        table = PrettyTable(['word', 'token_type'])
        for lex in lexemes:
            table.add_row([lex.word, lex.token_type])

        self.report([table])

        # terms = extract_terms(lexemes, count=10)

if __name__ == '__main__':
    c = Core()
    c.run('test.txt')

