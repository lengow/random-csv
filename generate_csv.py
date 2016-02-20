import argparse
import csv
import random
import string
import sys
from datetime import datetime

def integer_csv(filemask, addtime, rows, schema, delimiter, header, seed):
    if seed:
        random.seed(seed)
    generators = []
    filestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S.%f')[:-3]
    extension = '.txt'
    filename = filemask + '_' + filestamp + extension if addtime else filemask + extension

    char_set = (string.ascii_letters + string.digits +
                '"' + "'" + "#&* \t")

    head = []
    intcount, strcount, floatcount, ipcount, datecount = 0,0,0,0,0
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

    try:
        # test existence of file
        f = open(filename,'w',newline='')
        writer = csv.writer(f,delimiter=delimiter)
    except:
        writer = csv.writer(sys.stdout,delimiter=delimiter)
    with open(filename,'w') as f:
        if header:
            writer.writerow(head)
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
    parser.add_argument('--header', dest='header', action='store_true', required=False,
                        help='generate a simple header')
    parser.set_defaults(header=False)
    parser.add_argument('schema', type=str, nargs='+',
                        choices=['int', 'str', 'float', 'ip', 'date'],
                        help='list of column types to generate')

    args = parser.parse_args()
    for i in range(args.howmany):
        integer_csv(args.filemask, args.addtime, args.rows, args.schema, args.delimiter, args.header, args.seed)
