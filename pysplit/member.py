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
from .utils import now


class Member():
    def __init__(self, name, stamp=now()):
        self.name = name
        self.stamp = stamp

        self.purchases = []
        self.transfers = []
        self.receives = []

    def addPurchase(self, purchase):
        self.purchases.append(purchase)

    def addTransfer(self, transfer):
        self.transfers.append(transfer)

    def addReceive(self, receive):
        self.receives.append(receive)

    def _remove(self, x):
        if x in self.purchases:
            self.purchases.remove(x)
        if x in self.transfers:
            self.transfers.remove(x)
        if x in self.receives:
            self.receives.remove(x)

    @property
    def balance(self):
        return sum([x.amount for x in self.purchases + self.transfers]) - sum([x.amount_pp for x in self.receives])

    def _serialize(self):
        keys = ['name', 'stamp']
        return {key: getattr(self, key) for key in keys}

    def _reset(self):
        self.purchases = []
        self.transfers = []
        self.receives = []

    def __str__(self):
        str_info = '{:} - '.format(self.name)
        str_info += '{:} purchases - '.format(len(self.purchases))
        str_info += '{:} transfers - '.format(len(self.transfers))
        str_info += '{:} receives - '.format(len(self.purchases))
        str_info += '{:} balance'.format(self.balance)
        return str_info

    def __repr__(self):
        return '<{:} ({:}) - {:}>'.format(self.__class__.__name__, self.stamp, self)
