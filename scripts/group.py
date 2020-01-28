#!/usr/bin/env python3

# Split given items randomly into groups of (nearly) equal size.
# Support script for splitting files for annotators.

import sys
import os
import random


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('-m', '--max-size', metavar='N', type=int, default=None,
                    help='Maximum size of groups')
    ap.add_argument('-r', '--repeat', metavar='N', type=int, default=1,
                    help='Repeat each file N times in different groups')
    ap.add_argument('-s', '--seed', metavar='N', type=int, default=None,
                    help='Random seed')
    ap.add_argument('groups', type=int,
                    help='Number of groups of files to create')
    ap.add_argument('item', nargs='+')
    return ap


def group(items, group_num, options):
    if len(set(items)) != len(items):
        raise ValueError('duplicate(s) in input')
    groups = [[] for i in range(group_num)]
    candidates = []
    random.shuffle(items)
    for i in items:
        for r in range(options.repeat):
            if not candidates:
                for g in range(group_num):
                    if (options.max_size is None or
                        len(groups[g]) < options.max_size):
                        candidates.append(g)
                if not candidates:
                    break    # all full
            while True:
                g = random.choice(candidates)
                if i not in groups[g]:
                    groups[g].append(i)
                    candidates.remove(g)
                    break
            if min(len(g) for g in groups) == options.max_size:
                break
    return groups


def main(argv):
    args = argparser().parse_args(argv[1:])
    random.seed(args.seed)
    if args.repeat > args.groups:
        raise ValueError('repeat > groups')
    groups = group(args.item, args.groups, args)
    print('Divided {} items into {} groups (repeat {}), average size {}'.\
          format(len(args.item), len(groups), args.repeat,
                 sum(len(g) for g in groups)/len(groups)), file=sys.stderr)
    for g in groups:
        print(' '.join(list(g)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
