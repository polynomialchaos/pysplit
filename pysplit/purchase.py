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
from .utils import at_least_list, BaseClass, encode_datetime, datetime_to_string, decode_datetime, now
from .member import Member


class Purchase(BaseClass):
    def __init__(self, group, purchaser, recipients, amount, date=now(),
                 title='untitled', description='', stamp=now()):
        super().__init__(stamp=stamp)
        self.group = group
        self.purchaser = purchaser
        self.recipients = recipients
        self.amount = amount
        self.date = date
        self.title = title
        self.description = description

        self._link()

    def __del__(self):
        self._remove_link()

    def __str__(self):
        tmp = '{:}'.format(self.title)
        if self.description:
            tmp += ' ({:})'.format(self.description)
        tmp += ' {:}: {:} -> {:}'.format(self.purchaser.name,
                                         self.amount, ', '.join(self.recipients.keys()))
        return tmp

    def _link(self):
        self.purchaser.add_purchase(self)
        for recipient in self.recipients:
            self.recipients[recipient].add_receive(self)

    def _remove_link(self):
        self.purchaser.remove_purchase(self)
        for recipient in self.recipients:
            self.recipients[recipient].remove_receive(self)

    def _serialize(self):
        return {
            'purchaser': self.purchaser.name,
            'recipients': [x for x in self.recipients],
            'amount': self.amount,
            'date': self.date,
            'title': self.title,
            'description': self.description
        }

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, x):
        self._amount = float(x)

    @property
    def date(self):
        tmp = decode_datetime(self._date)
        return datetime_to_string(tmp)

    @date.setter
    def date(self, x):
        self._date = encode_datetime(x)

    def get_recipient_amounts(self):
        return {key: self.get_member_amount(key) for key in self.recipients}

    def get_member_amount(self, name):
        if name not in self.recipients:
            return 0.0

        return self.amount / self.number_of_recipients

    @property
    def number_of_recipients(self):
        return len(self.recipients)

    @property
    def purchaser(self):
        return self._purchaser

    @purchaser.setter
    def purchaser(self, x):
        self._purchaser = self.group.get_member(x)

    @property
    def recipients(self):
        return self._recipients

    @recipients.setter
    def recipients(self, x):
        x = at_least_list(x)
        self._recipients = {xx: self.group.get_member(xx) for xx in x}
