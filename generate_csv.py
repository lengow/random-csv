import argparse
import csv
import random
import string
import sys
from datetime import datetime


def integer_csv(filemask, addtime, rows, schema, delimiter, seed):
    if seed:
        random.seed(seed)
    generators = []
    filestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S.%f')[:-3]
    extension = '.txt'
    filename = filemask + '_' + filestamp + extension if addtime else filemask + extension

    char_set = (string.ascii_letters + string.digits +
                '"' + "'" + "#&* \t")

    for column in schema:
        if column == 'int':
            generators.append(lambda: random.randint(0, 1e9))
        elif column == 'str':
            generators.append(lambda: ''.join(
                random.choice(char_set) for _ in range(12)))
        elif column == 'float':
            generators.append(lambda: random.random())

    try:
        # test existence of file
        f = open(filename,'w',newline='')
        writer = csv.writer(f,delimiter=delimiter)
    except:
        writer = csv.writer(sys.stdout,delimiter=delimiter)
        # TODO write header
        # writer.writerow(header)
    with open(filename,'w') as f:
        for x in range(rows):
            writer.writerow([g() for g in generators])


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
    parser.add_argument('schema', type=str, nargs='+',
                        choices=['int', 'str', 'float'],
                        help='list of column types to generate')

    args = parser.parse_args()
    for i in range(args.howmany):
        integer_csv(args.filemask, args.addtime, args.rows, args.schema, args.delimiter, args.seed)
