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
import json
from .utils import BaseClass, DuplicateMemberError, NoMemberError, NoValidMemberNameError, now
from .member import Member
from .purchase import Purchase
from .transfer import Transfer
from .balance import Balance


class Group(BaseClass):
    def __call__(self):
        mainrule = ''.join('=' for _ in range(80))
        rule = ''.join('-' for _ in range(80))

        print(mainrule)
        print('Group: {:}'.format(self.name))
        if self.description:
            print(self.description)

        print(mainrule)
        print('Turnover: {:}'.format(self.turnover))

        print(rule)
        print('Members:')
        for m in self.members:
            print(' * {:}'.format(self.members[m]))

        print(rule)
        print('Purchases:')
        for p in self.purchases:
            print(' * {:}'.format(p))

        print(rule)
        print('Transfers:')
        for t in self.transfers:
            print(' * {:}'.format(t))

        print(rule)
        print('Pending balances:')
        for b in self.balances():
            print(' * {:}'.format(b))

        print(mainrule)

    def __init__(self, name, description='', stamp=now()):
        super().__init__(stamp=stamp)
        self.name = name
        self.description = description

        self.members = {}
        self.purchases = []
        self.transfers = []

    def __str__(self):
        tmp = '{:}'.format(self.name)
        if self.description:
            tmp += '({:})'.format(self.description)
        return tmp

    def _serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'members': [m.to_dict() for m in self.members.values()],
            'purchases': [p.to_dict() for p in self.purchases],
            'transfers': [t.to_dict() for t in self.transfers],
        }

    def add_member(self, name, stamp=now()):
        if not name:
            raise(NoValidMemberNameError('Empty member name provided!'))

        if name in self.members:
            raise(DuplicateMemberError(name, self.members.keys()))

        self.members[name] = Member(self, name, stamp=stamp)

    def add_purchase(self, purchaser, recipients, amount, date=now(),
                     title='untitled', description='', stamp=now()):
        tmp = Purchase(self, purchaser, recipients, amount, date=date,
                       title=title, description=description, stamp=stamp)

        self.purchases.append(tmp)
        return tmp

    def add_transfer(self, purchaser, recipients, amount, date=now(),
                     title='untitled', description='', stamp=now()):
        tmp = Transfer(self, purchaser, recipients, amount, date=date,
                       title=title, description=description, stamp=stamp)

        self.transfers.append(tmp)
        return tmp

    def balances(self):
        balances = []

        ranked = sorted(self.members.values(), key=(lambda x: x.balance))
        balance_add = {x.name: 0 for x in ranked}

        for sender in ranked:
            for receiver in reversed(ranked):
                if sender == receiver:
                    continue
                sender_balance = sender.balance + balance_add[sender.name]
                receiver_balance = receiver.balance + \
                    balance_add[receiver.name]

                if receiver_balance > 0:
                    balance = min(abs(sender_balance), receiver_balance)
                    balance_add[sender.name] += balance
                    balance_add[receiver.name] -= balance

                    balances.append(
                        Balance(self, sender.name, receiver.name, balance)
                    )

        return balances

    def get_member(self, name):
        try:
            return self.members[name]
        except KeyError:
            raise(NoMemberError(name, self.members.keys()))

    def save(self, path, indent=None):
        with open(path, 'w') as fp:
            json.dump(self.to_dict(), fp, indent=indent)

    @property
    def turnover(self):
        return sum(x.amount for x in self.purchases)


def load_group(path):
    with open(path, 'r') as fp:
        data = json.load(fp)

    group = Group(
        data['name'], description=data['description'], stamp=data['stamp'])

    for member in data['members']:
        group.add_member(member['name'], stamp=member['stamp'])

    for purchase in data['purchases']:
        group.add_purchase(purchase['purchaser'], purchase['recipients'], purchase['amount'], date=purchase['date'],
                           title=purchase['title'], description=purchase['description'], stamp=purchase['stamp'])

    for transfer in data['transfers']:
        group.add_transfer(transfer['purchaser'], transfer['recipients'], transfer['amount'], date=transfer['date'],
                           title=transfer['title'], description=transfer['description'], stamp=transfer['stamp'])

    return group
