# MIT License
#
# Copyright (c) 2022 Florian Eigentler
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
from .utils import Base, DuplicateMemberError, MissingExchangeRateError, TimeStamp
from .utils import InvalidMemberError, InvalidMemberNameError
from .utils import Currency
from .member import Member
from .purchase import Purchase
from .transfer import Transfer
from .balance import Balance


class Group(Base):
    """Group class derived from pysplit base class."""

    def __call__(self):
        mainrule = ''.join('=' for _ in range(80))
        rule = ''.join('-' for _ in range(80))

        print(mainrule)
        print('Summary for group: {:}'.format(self.name))
        if self.description:
            print(self.description)

        print(mainrule)
        print(' * Turnover: {:.2f}{:}'.format(self.turnover, self.currency))

        if self.exchange_rates:
            print(rule)
            print('Exchange rates:')
            for c, c_r in self.exchange_rates.items():
                print(' * 1{:} -> {:}{:}'.format(self.currency, c_r, c))

        print(rule)
        print('Members:')
        for m in self._members:
            print(' * {:}'.format(self._members[m]))

        print(rule)
        print('Purchases:')
        for p in self._purchases:
            print(' * {:}'.format(p))

        print(rule)
        print('Transfers:')
        for t in self._transfers:
            print(' * {:}'.format(t))

        print(rule)
        print('Pending balances:')
        for b in self.balances():
            print(' * {:}'.format(b))

        print(mainrule)

    def __init__(self, name, description='', currency=Currency.Euro):
        """Group class initialization.

        Keyword arguments:
        name -- group name
        description -- group description (default '')
        currency -- group currency enum object (default Euro)
        """
        super().__init__()
        self.name = name
        self.description = description
        self.currency = currency

        self.exchange_rates = {}
        self._members = {}
        self._purchases = []
        self._transfers = []

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
            'members': [m.to_dict() for m in self._members.values()],
            'purchases': [p.to_dict() for p in self._purchases],
            'transfers': [t.to_dict() for t in self._transfers],
            'exchange_rates': {
                k.name: v for k, v in self.exchange_rates.items()}
        }

    def add_member(self, name):
        """Add a member to the group.

        Keyword arguments:
        name -- member name
        """
        if not name or name.isspace():
            raise(InvalidMemberNameError('Empty member name provided!'))

        if name in self._members:
            raise(DuplicateMemberError(name, self._members.keys()))

        tmp = Member(name)
        self._members[name] = tmp
        return tmp

    def add_purchase(self, title, purchaser, recipients, amount, currency, date):
        """Add a purchase to the group.

        Keyword arguments:
        title -- purchase title
        purchaser -- purchaser name
        recipients -- list of recipient names
        amount -- purchase amount
        currency -- purchase currency
        date -- a TimeStamp object
        """
        tmp = Purchase(self, title, purchaser,
                       recipients, amount, currency, date)
        self._purchases.append(tmp)
        return tmp

    def add_transfer(self, title, purchaser, recipient, amount, currency, date):
        """Add a transfer to the group.

        Keyword arguments:
        title -- transfer title
        purchaser -- purchaser name
        recipients -- recipient name or list of recipient names
        amount -- transfer amount
        currency -- transfer currency
        date -- a TimeStamp object
        """
        tmp = Transfer(self, title, purchaser,
                       recipient, amount, currency, date)
        self._transfers.append(tmp)
        return tmp

    def balances(self):
        """Generate the balance transfers and return a list of them."""
        balances = []

        ranked = sorted(self._members.values(), key=(lambda x: x.balance))
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
                            balance, self.currency, TimeStamp())
                    )

        return balances

    def exchange(self, amount, from_c):
        """Convert an amount in currency from_c to currency to_c.

        Keyword arguments:
        amount -- amount
        from_c -- from currency object
        """
        if from_c == self.currency:
            return amount
        else:
            if from_c not in self.exchange_rates:
                raise(MissingExchangeRateError(from_c))

            return amount / self.exchange_rates[from_c]

    def get_member_by_name(self, name):
        """Find and return a member object by name.

        Keyword arguments:
        name -- name string
        """
        try:
            return self._members[name]
        except KeyError:
            raise(InvalidMemberError(name, self._members.keys()))

    @property
    def number_of_members(self):
        """Return the number of members."""
        return len(self._members)

    def save(self, path, indent=4):
        with open(path, 'w') as fp:
            json.dump(self.to_dict(), fp, indent=indent)

    @ property
    def turnover(self):
        return sum(x.amount for x in self._purchases)


def load_group(path):
    """Load a group object from a specified JSON file and return dict object.

    Keyword arguments:
    path -- JSON file path
    """
    with open(path, 'r') as fp:
        data = json.load(fp)

    # group
    group = Group(
        data['name'],
        description=data['description'],
        currency=Currency[data['currency']]
    )
    group.set_time(data['stamp'])

    # exchange_rates
    for k, v in data['exchange_rates'].items():
        group.exchange_rates[Currency[k]] = v

    for member in data['members']:
        tmp = group.add_member(member['name'])
        tmp.set_time(member['stamp'])

    for purchase in data['purchases']:
        tmp = group.add_purchase(purchase['title'],
            purchase['purchaser'], purchase['recipients'],
            purchase['amount'], currency=Currency[purchase['currency']],
            date=TimeStamp(purchase['date']))
        tmp.set_time(purchase['stamp'])

    for transfer in data['transfers']:
        tmp = group.add_transfer(transfer['title'],
            transfer['purchaser'], transfer['recipients'][0],
            transfer['amount'], currency=Currency[transfer['currency']],
            date=TimeStamp(transfer['date']))
        tmp.set_time(transfer['stamp'])

    return group
