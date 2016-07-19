from time import time
from datetime import datetime
from prettytable import PrettyTable

from tokenizer import Tokenizer


def load_text(filename, debug=False):
    t = Tokenizer()

    with open(filename, 'r') as f:
        text = f.read()
        token_list = t.get_tokens(text, debug=debug)

    word_list = []
    for value in token_list:
        if value.type == 'word' or value.type == 'number':
            word_list.append(value)

    return text, token_list, word_list


def extract_terms(word_list, count=0, debug=False):

    term_list = dict()
    for word in word_list:

        if 'NOUN' in word.tag:
            if word.normal_form in term_list:
                term_list[word.normal_form] += 1
            else:
                term_list[word.normal_form] = 1

        if debug:
            print('{} {}:: {}'.format(word, (25 - len(word)) * ' ', word.tag))

    term_list = list(reversed(sorted(term_list.items(), key=lambda x: x[1]))) # ????

    return term_list if count == 0 else term_list[:count]


def get_sentences(token_list):
    sentence_list = []
    for t in token_list:
        pass

    return sentence_list


if __name__ == '__main__':
    raw, tokens, words = load_text('test.txt')

    table = PrettyTable(['word', 'type'])
    for t in tokens:
        table.add_row([t.word, t.type])

    rt = datetime.fromtimestamp(time())
    print(table, file=open('{}.{}_{}.{}.txt'.format(rt.day, rt.month, rt.hour, rt.minute), 'w'))

    #sentences = get_sentences(tokens)
    #for s in sentences:
    #    for word in s:
    #        print(word.word, sep=' ')
    #
    #    print()

    #terms = extract_terms(words, count=10)
    #print(terms)
