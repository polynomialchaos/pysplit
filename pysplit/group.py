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
from .utils import BaseClass, DuplicateMemberError, MissingExchangeRateError, InvalidMemberError, InvalidMemberNameError
from .utils import Currency, now
from .member import Member
from .purchase import Purchase
from .transfer import Transfer
from .balance import Balance


class Group(BaseClass):
    """Group class derived from pysplit base class."""

    def __call__(self):
        mainrule = ''.join('=' for _ in range(80))
        rule = ''.join('-' for _ in range(80))

        print(mainrule)
        print('Group: {:}'.format(self.name))
        if self.description:
            print(self.description)

        print(mainrule)
        print('Turnover: {:.2f}{:}'.format(self.turnover, self.currency))

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

    def __init__(self, name, description='', currency=Currency.Euro, exchange_rates={}, stamp=now()):
        """Group class initialization.

        Keyword arguments:
        name -- group name
        description -- group description (default '')
        currency -- group currency enum object (default Euro)
        exchange_rates -- group exchange rates (default {})
        stamp -- a datetime object, a serialized datetime object or a datetime string (default now())
        """
        super().__init__(stamp=stamp)
        self.name = name
        self.description = description
        self.currency = currency
        self.exchange_rates = exchange_rates

        self.members = {}
        self.purchases = []
        self.transfers = []

    def __str__(self):
        tmp = '{:}'.format(self.name)
        if self.description:
            tmp += '({:})'.format(self.description)
        return tmp

    def _serialize(self):
        """Convert the object to a JSON conform dictionary and return it."""
        return {
            'name': self.name,
            'description': self.description,
            'currency': self.currency.name,
            'members': [m.to_dict() for m in self.members.values()],
            'purchases': [p.to_dict() for p in self.purchases],
            'transfers': [t.to_dict() for t in self.transfers],
            'exchange_rates': {k.name: {kk.name: vv for kk, vv in v.items()} for k, v in self.exchange_rates.items()}
        }

    def add_member(self, name, stamp=now()):
        """Add a member to the group.

        Keyword arguments:
        name -- member name
        stamp -- a datetime object, a serialized datetime object or a datetime string (default now())
        """
        if not name:
            raise(InvalidMemberNameError('Empty member name provided!'))

        if name in self.members:
            raise(DuplicateMemberError(name, self.members.keys()))

        self.members[name] = Member(self, name, stamp=stamp)

    def add_purchase(self, purchaser, recipients, amount, date=now(),
                     title='untitled', description='', currency=None, stamp=now()):
        """Add a purchase to the group.

        Keyword arguments:
        purchaser -- purchaser name
        recipients -- recipient name or list of recipient names
        amount -- purchase amount
        date -- a datetime object, a serialized datetime object or a datetime string (default now())
        title -- purchase title (default 'untitled')
        description -- purchase description (default '')
        currency -- purchase currency (default None = group currency)
        stamp -- a datetime object, a serialized datetime object or a datetime string (default now())
        """

        tmp = Purchase(self, purchaser, recipients, amount, date=date,
                       title=title, description=description, currency=currency, stamp=stamp)

        self.purchases.append(tmp)
        return tmp

    def add_transfer(self, purchaser, recipients, amount, date=now(),
                     title='untitled', description='', currency=None, stamp=now()):
        """Add a transfer to the group.

        Keyword arguments:
        purchaser -- purchaser name
        recipients -- recipient name or list of recipient names
        amount -- transfer amount
        date -- a datetime object, a serialized datetime object or a datetime string (default now())
        title -- transfer title (default 'untitled')
        description -- transfer description (default '')
        currency -- transfer currency (default None = group currency)
        stamp -- a datetime object, a serialized datetime object or a datetime string (default now())
        """
        tmp = Transfer(self, purchaser, recipients, amount, date=date,
                       title=title, description=description, currency=currency, stamp=stamp)

        self.transfers.append(tmp)
        return tmp

    def balances(self):
        """Generate the balance transfers and return a list of them."""
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
                        Balance(self, sender.name, receiver.name,
                                balance, currency=self.currency)
                    )

        return balances

    def exchange(self, amount, from_c, to_c):
        """Convert an amount in currency from_c to currency to_c.

        Keyword arguments:
        amount -- amount
        from_c -- from currency object
        to_c -- to currency object
        """
        if from_c == to_c:
            return amount
        elif from_c in self.exchange_rates:
            return amount * self.exchange_rates[from_c][to_c]
        elif to_c in self.exchange_rates:
            return amount / self.exchange_rates[to_c][from_c]
        else:
            raise(MissingExchangeRateError(from_c, to_c))

    def get_member(self, name):
        """Find and return a member object by name.

        Keyword arguments:
        name -- name string
        """
        try:
            return self.members[name]
        except KeyError:
            raise(InvalidMemberError(name, self.members.keys()))

    def save(self, path, indent=None):
        with open(path, 'w') as fp:
            json.dump(self.to_dict(), fp, indent=indent)

    @ property
    def turnover(self):
        return sum(x.amount for x in self.purchases)


def load_group(path):
    """Load a group object from a specified JSON file and return dict object.

    Keyword arguments:
    path -- JSON file path
    """
    with open(path, 'r') as fp:
        data = json.load(fp)

    exchange_rates = {Currency[k]: {Currency[kk]: vv for kk, vv in v.items()}
                      for k, v in data['exchange_rates'].items()}

    group = Group(
        data['name'], description=data['description'], currency=Currency[data['currency']],
        exchange_rates=exchange_rates, stamp=data['stamp']
    )

    for member in data['members']:
        group.add_member(member['name'], stamp=member['stamp'])

    for purchase in data['purchases']:
        group.add_purchase(purchase['purchaser'], purchase['recipients'], purchase['amount'], date=purchase['date'],
                           title=purchase['title'], description=purchase['description'],
                           currency=Currency[purchase['currency']], stamp=purchase['stamp'])

    for transfer in data['transfers']:
        group.add_transfer(transfer['purchaser'], transfer['recipients'], transfer['amount'], date=transfer['date'],
                           title=transfer['title'], description=transfer['description'],
                           currency=Currency[transfer['currency']], stamp=transfer['stamp'])

    return group
