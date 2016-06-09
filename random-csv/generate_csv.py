import argparse
import csv
import random
import string
import sys
from datetime import datetime
from enum import Enum

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

def integer_csv(filemask, addtime, rows, schema, delimiter, sentence_max_size, header, seed):
    wg = namealizer.WordGenerator(seed=seed)
    generators = []
    filestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S.%f')[:-3]
    extension = '.txt'
    filename = filemask + '_' + filestamp + extension if addtime else filemask + extension

    char_set = (string.ascii_letters + string.digits + ' ')
    # '' + "'" + "#&* \t")

    head = []
    intcount, strcount, floatcount, ipcount, datecount, wordcount, pipewordscount, = 0,0,0,0,0,0,0
    namecount, levelcount, degreecount, sentencecount, urlcount = 0,0,0,0,0
    for column in schema:
        if column == 'int':
            intcount += 1
            head.append('number_' + str(intcount))
            generators.append(lambda: random.randint(0, 1e9))
        elif column == 'str':
            strcount += 1
            head.append('text_' + str(strcount))
            generators.append(lambda: ''.join(
                random.choice(char_set) for _ in range(12)))
        elif column == 'float':
            floatcount += 1
            head.append('float_' + str(floatcount))
            generators.append(lambda: random.random())
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
        elif column == 'pipewords':
            wordcount += 1
            head.append('labels_' + str(pipewordscount))
            generators.append(lambda: ''.join(
                generatepipewords(wg)
            ))
        elif column == 'sentence':
            wordcount += 1
            head.append('labels_' + str(sentencecount))
            generators.append(lambda: ''.join(
                generatesentence(sentence_max_size, wg)
            ))
        elif column == 'url':
            wordcount += 1
            head.append('labels_' + str(urlcount))
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
                             random.randint(1,99),
                             "″",
                             " ",
                             CardinalNS(random.randint(1,2)).name))),
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
                             random.randint(1,99),
                             "″",
                             " ",
                             CardinalEW(random.randint(1,2)).name))),
            ))


        # # // deal with csv limitation for delimiter var
        #             doesn't work!
        #         if delimiter=='\\t':
        #             delimiter='\t'

    try:
        f = open(filename,'w',newline='', encoding='utf-8')
        writer = csv.writer(f,delimiter=delimiter)
    except:
        writer = csv.writer(sys.stdout,delimiter=delimiter)
    with open(filename,'w') as f:
        if header:
            writer.writerow(head)
        for x in range(rows):
            writer.writerow([g() for g in generators])

def generateword(wg):
    return wg[1]

def generatesentence(max_nb_words, wg):
    sentence_size = random.randint(1, max_nb_words)
    words = wg[sentence_size]
    return words

def generatepipewords(wg):
    words = generatesentence(3, wg)
    retval = words.replace(' ','|')
    return retval

def generateurl(wg):
    domain_gen = generatesentence(2, wg)
    domain = domain_gen.replace(' ','.')+'.'+generateword(wg)[:3]
    path_gen = generatesentence(5, wg)
    path = path_gen.replace(' ','/')
    file = generateword(wg)+'.'+generateword(wg)[:3]
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
    parser.set_defaults(header=False)
    parser.add_argument('schema', type=str, nargs='+',
                        choices=['int', 'str', 'float', 'ip', 'date', 'word', 'pipewords', 'name', 'level', 'lat',
                                 'long', 'sentence', 'url'],
                        help='list of column types to generate')

    args = parser.parse_args()
    for i in range(args.howmany):
        sys.stdout.write('file ' + str(i) + '\n')
        integer_csv(args.filemask, args.addtime, args.rows, args.schema, args.delimiter, args.sentence_max_size,
                    args.header, args.seed)