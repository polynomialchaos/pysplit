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
    def __init__(self, group, name, stamp=now()):
        super().__init__(stamp=stamp)
        self.group = group
        self.name = name

        self.purchases = []
        self.transfers = []
        self.receives = []

    def __str__(self):
        return '{:} ({:.2f}{:})'.format(self.name, self.balance, self.group.currency)

    def _serialize(self):
        return {
            'name': self.name
        }

    def add_purchase(self, purchase):
        self.purchases.append(purchase)

    def add_transfer(self, transfer):
        self.transfers.append(transfer)

    def add_receive(self, receive):
        self.receives.append(receive)

    @property
    def balance(self):
        balance = sum([x.amount for x in self.purchases])
        balance += sum([x.amount for x in self.transfers])
        balance -= sum([x.get_member_amount(self.name)
                       for x in self.receives])
        return balance

    def remove_purchase(self, purchase):
        self.purchases.remove(purchase)

    def remove_transfer(self, transfer):
        self.transfers.remove(transfer)

    def remove_receive(self, receive):
        self.receives.remove(receive)
