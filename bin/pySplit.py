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
from pysplit import Group, loadJson


def main():
   # define the argument parser
    parser = argparse.ArgumentParser(
        description='pySplit - Cash sharing library')
    parser.add_argument('-m', '--member', dest='member', required=False,
                        action='store_true', help='Add a member to the group')
    parser.add_argument('-p', '--purchase', dest='purchase', required=False,
                        action='store_true', help='Add a purchase to the group')
    parser.add_argument('-t', '--transfer', dest='transfer', required=False,
                        action='store_true', help='Add a transfer to the group')
    parser.add_argument('path', nargs='?', help='The path to a group file')
    args = parser.parse_args()

    # load or create a group
    if args.path:
        group = loadJson(args.path)
    else:
        inp_name = input(' >>> Group name: ')
        inp_description = input(' >>> Group description: ')
        group = Group(inp_name, description=inp_description)

    if args.member:
        inp_name = input(' >>> Member name: ')
        inp_names = inp_name.split(';')
        for x in inp_names:
            group.addMember(x)

    if args.purchase:
        inp_name = input(' >>> Purchase name: ')
        inp_description = input(' >>> Purchase description: ')
        inp_amount = input(' >>> Purchase amount: ')
        inp_purchaser = input(' >>> Purchase purchaser: ')
        inp_recipients = input(' >>> Purchase recipients: ')
        group.addPurchase(inp_purchaser, inp_recipients.split(
            ';'), float(inp_amount), inp_name, inp_description)

    if args.transfer:
        inp_name = input(' >>> Transfer name: ')
        inp_description = input(' >>> Transfer description: ')
        inp_amount = input(' >>> Transfer amount: ')
        inp_purchaser = input(' >>> Transfer purchaser: ')
        inp_recipient = input(' >>> Transfer recipient: ')
        group.addTransfer(inp_purchaser, inp_recipient, float(
            inp_amount), inp_name, inp_description)

    # print the results
    for p in group.purchases:
        print(p)

    for t in group.transfers:
        print(t)

    group.printBalance()

    # store the group in the existing file or create a new one
    if args.path:
        group.save(args.path)
    else:
        inp_name = input(' >>> Group file name: ')
        if not inp_name:
            inp_name = '{:}.json'.format(group.name)
        group.save(inp_name)


if __name__ == '__main__':
    main()
