import pymorphy2
from tokenizer import Tokenizer


def load_text(filename, debug=False):

    t = Tokenizer()
    with open(filename, 'r') as f:
        raw = f.read()
        # Нужна постобработка
        # (Склейка устойчивых словосочитаний)
        word_list = t.get_words2(raw, debug=debug)

    return word_list, raw


def extract_terms(word_list, count=0, debug=False):

    morph = pymorphy2.MorphAnalyzer()
    term_list = dict()
    for word in word_list:
        t = morph.parse(word)[0]
        if 'NOUN' in t.tag:
            if t.normal_form in term_list:
                term_list[t.normal_form] += 1
            else:
                term_list[t.normal_form] = 1

        if debug:
            print('{} {}:: {}'.format(word, (25 - len(word)) * ' ', t.tag))

    term_list = list(reversed(sorted(term_list.items(), key=lambda x: x[1])))

    return term_list if count == 0 else term_list[:count]


if __name__ == '__main__':
    words, _ = load_text('test.txt')
    print(words)

    terms = extract_terms(words, count=10)
    print(terms)
