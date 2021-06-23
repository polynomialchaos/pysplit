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
from .utils import BaseClass, now


class Member(BaseClass):
    """Member class derived from pysplit base class."""

    def __init__(self, group, name, stamp=now()):
        """Member class initialization.

        Keyword arguments:
        group -- group object
        name -- member name
        stamp -- a datetime object, a serialized datetime object or a datetime string (default now())
        """
        super().__init__(stamp=stamp)
        self.group = group
        self.name = name

        self.purchases = []
        self.transfers = []
        self.receives = []

    def __str__(self):
        return '{:} ({:.2f}{:})'.format(self.name, self.balance, self.group.currency)

    def _serialize(self):
        """Convert the object to a JSON conform dictionary and return it."""
        return {
            'name': self.name
        }

    def add_purchase(self, purchase):
        """Add a purchase reference to the member.

        Keyword arguments:
        purchase -- a purchase object reference
        """
        self.purchases.append(purchase)

    def add_receive(self, receive):
        """Add a receive reference to the member.

        Keyword arguments:
        receive -- a purchase of transfer object reference
        """
        self.receives.append(receive)

    def add_transfer(self, transfer):
        """Add a transfer reference to the member.

        Keyword arguments:
        transfer -- a transfer object reference
        """
        self.transfers.append(transfer)

    @property
    def balance(self):
        """Calculate the member balance and return the value in groups currency."""
        balance = sum([x.amount for x in self.purchases])
        balance += sum([x.amount for x in self.transfers])
        balance -= sum([x.get_member_amount(self.name)
                       for x in self.receives])
        return balance

    def remove_purchase(self, purchase):
        """Remove a purchase reference from the member.

        Keyword arguments:
        transfer -- a purchase object reference
        """
        self.purchases.remove(purchase)

    def remove_receive(self, receive):
        """Remove a receive reference from the member.

        Keyword arguments:
        transfer -- a purchase or transfer object reference
        """
        self.receives.remove(receive)

    def remove_transfer(self, transfer):
        """Remove a transfer reference from the member.

        Keyword arguments:
        transfer -- a transfer object reference
        """
        self.transfers.remove(transfer)
