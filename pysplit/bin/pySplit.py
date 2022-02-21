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
# import logging
import sys
from pysplit import *
from pysplit.utils import Currency, InvalidMemberError, now
from pysplit.utils.stamp import datetime_to_string


def user_input(description, default=None, options=None, func=str):
    """Parse user input. Use default value, show options and parse output."""
    def_str = '[{:}]'.format(default) if default else ''
    des_str = ' '.join([description, def_str]).strip()

    opt_str = '({:})'.format(', '.join(options)) if options else ''
    des_str = ' '.join([des_str, opt_str]).strip()

    inp_data = input('{:}: '.format(des_str)) or default
    if inp_data is None:
        raise(ValueError('Required input not provided!'))

    return func(inp_data)


def main():
    # define the argument parser
    parser = argparse.ArgumentParser(
        description='pySplit - A simple python package for money pool split development.')
    # parser.add_argument('-d', '--debug', dest='debug', required=False,
    #                     action='store_true', help='Provide logging output')
    parser.add_argument('-m', '--member', dest='member', required=False,
                        action='store_true', help='Add a member to the group.')
    parser.add_argument('-p', '--purchase', dest='purchase', required=False,
                        action='store_true', help='Add a purchase to the group.')
    parser.add_argument('-t', '--transfer', dest='transfer', required=False,
                        action='store_true', help='Add a transfer to the group.')
    parser.add_argument('path', nargs='?', help='The path to a group file.')
    args = parser.parse_args()

    # # logging
    # logger = logging.getLogger()
    # logger.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(levelname)s: %(message)s')
    # stdout_handler = logging.StreamHandler(sys.stdout)
    # stdout_handler.setLevel(logging.INFO)
    # stdout_handler.setFormatter(formatter)
    # logger.addHandler(stdout_handler)

    # if args.debug:
    #     file_handler = logging.FileHandler(
    #         '{:}.log'.format('output'), mode='w')
    #     file_handler.setFormatter(formatter)
    #     logger.addHandler(file_handler)

    # load or create a group
    if args.path:
        group = load_group(args.path)
    else:
        inp_title = user_input('Group title', default='Untitled')
        inp_description = user_input('Group description', default='')
        inp_currency = user_input('Group currency',
                                  default=Currency.Euro.name,
                                  options=[x.name for x in Currency],
                                  func=(lambda x: Currency[x]))

        group = Group(inp_title, description=inp_description,
                      currency=inp_currency)

    # add member(s)
    if args.member or not group.members:
        while True:
            inp_name = user_input(
                'Member name (Enter to continue)', default='')
            if inp_name:
                group.add_member(inp_name)
            else:
                break

    # add purchase(s)
    if args.purchase:
        if not group.members:
            raise InvalidMemberError('No members have been defined!')

        members = list(group.members.keys())
        while True:
            inp_title = user_input('Purchase title', default='Untitled')

            inp_purchaser = user_input('Purchaser', default=members[0],
                                       options=members)
            inp_recipients = user_input('Purchase recipients (seperated by ;)',
                                        default='; '.join(members),
                                        options=members,
                                        func=(lambda x: [
                                            xx.strip()
                                            for xx in x.split(';')
                                        ]))

            inp_amount = user_input('Purchase amount', func=float)
            inp_currency = user_input('Purchase currency',
                                      default=group.currency.name,
                                      options=[x.name for x in Currency],
                                      func=(lambda x: Currency[x]))

            inp_date = user_input(
                'Purchase date', default=datetime_to_string(now()))

            group.add_purchase(inp_title, inp_purchaser, inp_recipients,
                               inp_amount, date=inp_date,
                               currency=inp_currency)

            if not user_input('Add another purchase',
                              default='n', options=['y', 'N'],
                              func=(lambda x: x.lower() == 'y')):
                break

    # add transfer(s)
    if args.transfer:
        if not group.members:
            raise InvalidMemberError('No members have been defined!')

        members = list(group.members.keys())
        while True:
            inp_title = user_input('Transfer title', default='Untitled')

            inp_purchaser = user_input('Purchaser', default=members[0],
                                       options=members)
            inp_recipients = user_input('Transfer recipient',
                                        default=members[0],
                                        options=members)

            inp_amount = user_input('Transfer amount', func=float)
            inp_currency = user_input('Transfer currency',
                                      default=Currency.Euro.name,
                                      options=[x.name for x in Currency],
                                      func=(lambda x: Currency[x]))

            inp_date = user_input(
                'Transfer date', default=datetime_to_string(now()))

            group.add_transfer(inp_title, inp_purchaser, inp_recipients,
                               inp_amount, date=inp_date,
                               currency=inp_currency)

            if not user_input('Add another trajsfer',
                              default='n', options=['y', 'N'],
                              func=(lambda x: x.lower() == 'y')):
                break

    # print the group stats
    group()

    # store the group in the existing file or create a new one
    if args.path:
        file_path = args.path
    else:
        tmp = group.name.lower().replace(' ', '_')
        file_path = user_input('File name',
                               default='{:}.json'.format(tmp))

    group.save(file_path, indent=4)


if __name__ == '__main__':
    main()
