# MIT License
#
# Copyright (c) 2021 Florian
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import argparse
from pysplit import *
from pysplit.utils import NoValidMemberNameError, now


def main():
    # group = Group('test', 'a sample tsest')
    # group.add_member('Florian')
    # group.add_member('Floria2')
    # # print(group.get_member('Florian'))

    # # print(group.members)

    # sumi = 0
    # for i in range(10):
    #     p = group.add_purchase('Florian', ['Florian', 'Floria2'], i + 0.33)
    #     sumi += i

    # group()

    # define the argument parser
    parser = argparse.ArgumentParser(
        description='pysplit - A simple python package for money pool split development.')
    parser.add_argument('-m', '--member', dest='member', required=False,
                        action='store_true', help='Add a member to the group')
    parser.add_argument('-p', '--purchase', dest='purchase', required=False,
                        action='store_true', help='Add a purchase to the group')
    parser.add_argument('-t', '--transfer', dest='transfer', required=False,
                        action='store_true', help='Add a transfer to the group')
    parser.add_argument('path', nargs='?', help='The path to a group file')
    args = parser.parse_args()

    print(args.path)
    # load or create a group
    if args.path:
        group = load_group(args.path)
    else:
        inp_name = input(' >>> Group name: ')
        inp_description = input(' >>> Group description: ')
        group = Group(inp_name, description=inp_description)

    if args.member:
        while True:
            try:
                inp_name = input(' >>> Member name: ')
                group.add_member(inp_name)
            except NoValidMemberNameError:
                break

    if args.purchase:
        while True:
            inp_purchaser = input(' >>> Purchase purchaser: ')
            inp_recipients = input(
                ' >>> Purchase recipients (seperated by ;): ')
            inp_amount = input(' >>> Purchase amount: ')
            inp_date = input(' >>> Purchase date (opt): ')
            if not inp_date:
                inp_date = now()
            inp_title = input(' >>> Purchase title (opt): ')
            inp_description = input(' >>> Purchase description (opt): ')

            group.add_purchase(inp_purchaser, inp_recipients.split(';'), inp_amount, date=inp_date,
                               title=inp_title, description=inp_description, stamp=now())

            inp_cont = input(' >>> Add another purchase [Y/n]: ')
            if not inp_cont.lower() == 'y':
                break

    if args.transfer:
        while True:
            inp_purchaser = input(' >>> Transfer purchaser: ')
            inp_recipient = input(
                ' >>> Transfer recipient: ')
            inp_amount = input(' >>> Transfer amount: ')
            inp_date = input(' >>> Transfer date (opt): ')
            if not inp_date:
                inp_date = now()
            inp_title = input(' >>> Transfer title (opt): ')
            inp_description = input(' >>> Transfer description (opt): ')

            group.add_purchase(inp_purchaser, inp_recipient, inp_amount, date=inp_date,
                               title=inp_title, description=inp_description, stamp=now())

            inp_cont = input(' >>> Add another transfer [Y/n]: ')
            if not inp_cont.lower() == 'y':
                break

    # print the group stats
    group()

    # store the group in the existing file or create a new one
    if args.path:
        group.save(args.path, indent=4)
    else:
        inp_name = input(' >>> Group file name: ')
        if not inp_name:
            inp_name = '{:}.json'.format(group.name)
        group.save(inp_name, indent=4)


if __name__ == '__main__':
    main()
