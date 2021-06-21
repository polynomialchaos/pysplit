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
from .utils import now, ERROR
from .member import Member
from .purchase import Purchase
from .transfer import Transfer


class GROUP():
    def __init__(self, name, description='', stamp=now()):
        self.name = name
        self.description = description
        self.stamp = stamp

        self.members = []
        self.purchases = []
        self.transfers = []

    def getMember(self, name):
        for member in self.members:
            if member.name == name:
                return member

        raise ERROR('Could not locate member with name "{:}"!'.format(name))

    def addMember(self, name, stamp=now()):
        if name in [x.name for x in self.members]:
            raise ERROR('Provided duplicate member name "{:}"!'.format(name))

        self.members.append(Member(name.strip(), stamp=stamp))

    def addPurchase(self, purchaser, recipients, amount, name='', description='', stamp=now()):
        self.purchases.append(
            Purchase(self.getMember(purchaser.strip()), [self.getMember(x.strip()) for x in recipients], amount,
                     name=name, description=description, stamp=stamp)
        )

    def addTransfer(self, purchaser, recipient, amount, name='', description='', stamp=now()):
        self.transfers.append(
            Transfer(self.getMember(purchaser.strip()), self.getMember(recipient.strip()), amount,
                     name=name, description=description, stamp=stamp)
        )

    def save(self, path):
        with open(path, 'w') as f:
            json.dump(self._serialize(), f, indent=4)

    def _reset(self):
        for member in self.members:
            member._reset()
        self.balances = []

    def printBalance(self):
        tmpBalances = []
        self.members = sorted(self.members, key=(lambda x: x.balance))

        for member in self.members:
            for receiver in reversed(self.members):
                if receiver.balance > 0.0 and member.name != receiver.name:
                    tmpBalances.append(
                        Transfer(member, receiver, min(
                            abs(member.balance), receiver.balance), name='BALANCE')
                    )

        for balance in tmpBalances:
            print(repr(balance))
            balance._remove()

    def _serialize(self):
        keys = ['name', 'description', 'stamp']
        tmp = {key: getattr(self, key) for key in keys}
        tmp.update({'members': [x._serialize() for x in self.members]})
        tmp.update({'purchases': [x._serialize() for x in self.purchases]})
        tmp.update({'transfers': [x._serialize() for x in self.transfers]})
        return tmp

    def __str__(self):
        str_info = '{:} - '.format(self.name) if self.name else ''
        str_info += '{:} - '.format(self.description) if self.description else ''
        str_info += '{:} members - '.format(len(self.members))
        str_info += '{:} purchases - '.format(len(self.purchases))
        str_info += '{:} transfers'.format(len(self.transfers))
        return str_info

    def __repr__(self):
        return '<{:} ({:}) - {:}>'.format(self.__class__.__name__, self.stamp, self)


def loadJson(path):
    with open(path, 'r') as f:
        data = json.load(f)

    tmp = GROUP(data['name'], data['description'], data['stamp'])

    for member in data['members']:
        tmp.addMember(member['name'], stamp=member['stamp'])

    for purchase in data['purchases']:
        tmp.addPurchase(purchase['purchaser'], purchase['recipients'], purchase['amount'],
                        name=purchase['name'], description=purchase['description'], stamp=purchase['stamp'])

    for transfer in data['transfers']:
        tmp.addTransfer(transfer['purchaser'], transfer['recipients'][0], transfer['amount'],
                        name=transfer['name'], description=transfer['description'], stamp=transfer['stamp'])

    return tmp
