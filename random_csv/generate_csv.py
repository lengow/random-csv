import argparse
import csv
import random
import string
import sys
from collections import OrderedDict
from datetime import datetime
from enum import Enum
from functools import partial

import namealizer


class Level(Enum):
    CRITICAL = 1
    SEVERE = 2
    MODERATE = 3
    MILD = 4
    INFO = 5


class CardinalNS(Enum):
    N = 1
    S = 2


class CardinalEW(Enum):
    W = 1
    E = 2


def csv_generator(rows, schema, sentence_max_size, desc_max_size, categories_size, header, seed):
    """
    generator of random csv lines

    :param rows: number of rows in the file
    :param schema: description of the file columns, as a list of strings
    :param sentence_max_size: maximum number of words on random sentences
    :param desc_max_size: maximum number of words on random descriptions
    :param categories_size: number of elements in categories
    :param header: if header is displayed or not, boolean
    :param seed: seed for the random generators

    """

    # initializations of generators and charset
    wg = namealizer.WordGenerator(seed=seed)
    wg.dictionary = OrderedDict(sorted(wg.dictionary.items(), key=lambda x:x[1], reverse=True))
    generators = []
    char_set = (string.ascii_letters + string.digits + ' ')
    categories = []
    generated_ids = []
    def choose_category_element(i):
        return random.choice(categories[i])
    def choose_id_element(i):
        return generated_ids[i].pop()
    # '' + "'" + "#&* \t")

    # creation of the random generators + headers
    head = []
    intcount, strcount, floatcount, ipcount, datecount, wordcount, pipewordscount, desccount = 0, 0, 0, 0, 0, 0, 0, 0
    levelcount, degreecount, sentencecount, urlcount, idcount, categorycount = 0, 0, 0, 0, 0, 0
    for column in schema:
        if column == 'int':
            intcount += 1
            head.append('number_' + str(idcount))
            generators.append(lambda: random.randint(0, 1e9))
        if column == 'id':
            idcount += 1
            head.append('id_' + str(idcount))
            generated_ids.append(list_of_ids(rows))
            generators.append(partial(choose_id_element, idcount-1))
        elif column == 'str':
            strcount += 1
            head.append('text_' + str(strcount))
            generators.append(lambda: ''.join(
                random.choice(char_set) for _ in range(12)))
        elif column == 'float':
            floatcount += 1
            head.append('float_' + str(floatcount))
            generators.append(lambda: random.randint(0, 1e4)+random.random())
        elif column == 'ip':
            ipcount += 1
            head.append('ip_' + str(ipcount))
            # http://stackoverflow.com/a/21014713 Thanks jonrsharpe
            generators.append(lambda: ''.join(
                ".".join(map(str, (random.randint(0, 255)
                                   for _ in range(4))))
            ))
        elif column == 'date':
            datecount += 1
            head.append('date_' + str(datecount))
            generators.append(lambda: ''.join(
                datetime.fromtimestamp(random.randint(0, 1e10)).strftime("%d/%m/%y_%H:%M")
            ))
        elif column == 'word':
            wordcount += 1
            head.append('label_' + str(wordcount))
            generators.append(lambda: ''.join(
                generateword(wg)
            ))
        elif column == 'category':
            categorycount += 1
            elements = wg[categories_size]
            categories.append(elements.split())
            head.append('category_' + str(categorycount))
            generators.append(partial(choose_category_element, categorycount-1))
        elif column == 'pipewords':
            pipewordscount += 1
            head.append('pipe_' + str(pipewordscount))
            generators.append(lambda: ''.join(
                generatepipewords(wg)
            ))
        elif column == 'sentence':
            sentencecount += 1
            head.append('sentence_' + str(sentencecount))
            generators.append(lambda: ''.join(
                generatesentence(sentence_max_size, wg)
            ))
        elif column == 'description':
            desccount += 1
            head.append('description_' + str(desccount))
            generators.append(lambda: ''.join(
                generatesentence(desc_max_size, wg)
            ))
        elif column == 'url':
            urlcount += 1
            head.append('url_' + str(urlcount))
            generators.append(lambda: ''.join(
                generateurl(wg)
            ))
        elif column == 'level':
            levelcount += 1;
            head.append('level' + str(levelcount))
            generators.append(lambda: ''.join(
                Level(random.randint(1, 5)).name
            ))
        elif column == 'lat':
            head.append('latitude')
            generators.append(lambda: ''.join(
                "".join(map(str,
                            (random.randint(0, 89),
                             "°",
                             " ",
                             random.randint(0, 59),
                             "′",
                             " ",
                             random.randint(0, 59),
                             ".",
                             random.randint(1, 99),
                             "″",
                             " ",
                             CardinalNS(random.randint(1, 2)).name))),
            ))
        elif column == 'long':
            head.append('longitude')
            generators.append(lambda: ''.join(
                "".join(map(str,
                            (random.randint(0, 179),
                             "°",
                             " ",
                             random.randint(0, 59),
                             "′",
                             " ",
                             random.randint(0, 59),
                             ".",
                             random.randint(1, 99),
                             "″",
                             " ",
                             CardinalEW(random.randint(1, 2)).name))),
            ))

    # return the header at first call if specified
    if header:
        yield head

    # return randomly generated csv lines
    n = 0
    while n < rows:
        yield [g() for g in generators]
        n += 1


def list_of_ids(nb):
    """ generates a list of unique ids"""

    # sorted ids, with a random step between each
    ids_tmp = [random.randint(1, 100)]
    for _ in range(nb-1):
        ids_tmp.append(ids_tmp[-1]+random.randint(1, 100))

    # random mixing of the ids
    ids = []
    for i in range(nb):
        index = random.randint(0, nb-i-1)
        ids.append(ids_tmp[index])
        del ids_tmp[index]
    return ids


def generateword(wg):
    return wg[1]


def generatesentence(max_nb_words, wg):
    sentence_size = random.randint(1, max_nb_words)
    words = wg[sentence_size]
    return words


def generatepipewords(wg):
    words = generatesentence(3, wg)
    retval = words.replace(' ', '|')
    return retval


def generateurl(wg):
    domain_gen = generatesentence(2, wg)
    domain = domain_gen.replace(' ', '.') + '.' + generateword(wg)[:3]
    path_gen = generatesentence(3, wg)
    path = path_gen.replace(' ', '/')
    file = generateword(wg) + '.' + generateword(wg)[:3]
    retval = "/".join([random.choice(['http:/', 'https:/']), domain, path, file])
    return retval


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate a large CSV file.',
        epilog='''"Space is big. You just won't believe how vastly,
        hugely, mind-bogglingly big it is."''')
    parser.add_argument('--filemask', type=str, default='sys.stdout', required=False,
                        help='mask of filename (eg: "../test-csv") (empty=stdout)')
    parser.add_argument('--addtimestamp', dest='addtime', action='store_true', required=False,
                        help='choose whether to timestamp filename')
    parser.add_argument('--notimestamp', dest='addtime', action='store_false', required=False,
                        help='choose whether to timestamp filename')
    parser.set_defaults(addtime=False)
    parser.add_argument('rows', type=int,
                        help='number of rows to generate')
    parser.add_argument('--delimiter', type=str, default=',', required=False,
                        help='the CSV delimiter')
    parser.add_argument('--seed', type=int, required=False,
                        help='optional random seed')
    parser.add_argument('--how-many', dest='howmany', type=int, default=1, required=False,
                        help='how many files to generate. Default is 1')
    parser.add_argument('--header', dest='header', action='store_true', required=False,
                        help='generate a simple header')
    parser.add_argument('--sentence-max-size', dest='sentence_max_size', type=int, default=10, required=False,
                        help='maximum size of sentences. Default is 10')
    parser.add_argument('--description-max-size', dest='desc_max_size', type=int, default=100, required=False,
                        help='maximum size of sentences. Default is 100')
    parser.add_argument('--categories-size', dest='categories_size', type=int, default=10, required=False,
                        help='Number of elements in categories. Default is 10')
    parser.set_defaults(header=False)
    parser.add_argument('schema', type=str, nargs='+',
                        choices=['int', 'str', 'float', 'ip', 'date', 'word', 'pipewords', 'level', 'lat',
                                 'long', 'sentence', 'url', 'id', 'category', 'description'],
                        help='list of column types to generate')

    args = parser.parse_args()
    for i in range(args.howmany):
        sys.stdout.write('file ' + str(i) + '\n')
        schema = args.schema
        schema.extend(['word']*40)
        gen = csv_generator(args.rows, schema, args.sentence_max_size, args.desc_max_size, args.categories_size,
                            args.header, args.seed)

        filestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        extension = '.csv'
        filename = args.filemask + '_' + filestamp + extension if args.addtime else args.filemask + extension

        try:
            f = open(filename, 'w', newline='', encoding='utf-8')
            writer = csv.writer(f, delimiter=args.delimiter)
        except:
            writer = csv.writer(sys.stdout, delimiter=args.delimiter)
        with open(filename, 'w') as f:
            for line in gen:
                writer.writerow(line)

