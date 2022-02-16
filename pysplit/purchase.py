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
from .utils import at_least_list, BaseClass, encode_datetime, datetime_to_string, decode_datetime, now, Currency
from .member import Member


class Purchase(BaseClass):
    """Purchase class derived from base class.
    This derived class links in member purchases."""

    def __init__(self, group, purchaser, recipients, amount, date=now(),
                 title='untitled', currency=None, stamp=now()):
        """Purchase class initialization.

        Keyword arguments:
        group -- group object
        purchaser -- purchaser name
        recipients -- recipient name or list of recipient names
        amount -- purchase amount
        date -- a datetime object, a serialized datetime object or a datetime string (default now())
        title -- purchase title (default 'untitled')
        currency -- purchase currency (default None = group currency)
        stamp -- a datetime object, a serialized datetime object or a datetime string (default now())
        """
        super().__init__(stamp=stamp)
        self.group = group
        self.purchaser = purchaser
        self.recipients = recipients
        self.amount = amount
        self.currency = self.group.currency if currency is None else currency
        self.date = date
        self.title = title

        self._link()

    def __del__(self):
        self._remove_link()

    def __str__(self):
        tmp = '{:} ({:})'.format(self.title, self.date)
        tmp += ' {:}: {:.2f}{:} -> {:}'.format(self.purchaser.name,
                                               self._amount, self.currency,
                                               ', '.join(self.recipients.keys()))
        return tmp

    def _link(self):
        """Link the purchase object in the members objects."""
        self.purchaser.add_purchase(self)
        for recipient in self.recipients:
            self.recipients[recipient].add_receive(self)

    def _remove_link(self):
        """Remove the purchase object from the members objects.."""
        self.purchaser.remove_purchase(self)
        for recipient in self.recipients:
            self.recipients[recipient].remove_receive(self)

    def _serialize(self):
        """Convert the object to a JSON conform dictionary and return it."""
        return {
            'purchaser': self.purchaser.name,
            'recipients': [x for x in self.recipients],
            'amount': self._amount,
            'currency': self.currency.name,
            'date': self.date,
            'title': self.title
        }

    @property
    def amount(self):
        return self.group.exchange(self._amount, self.currency)

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

    def get_member_amount(self, name):
        """Calculate the member amount in group currency and return it."""
        if name not in self.recipients:
            return 0.0

        return self.amount / self.number_of_recipients

    @property
    def number_of_recipients(self):
        """Return the number of recipients."""
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
