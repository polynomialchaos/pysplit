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
from .utils import at_least_1d, Base


class Purchase(Base):
    """Purchase class derived from base class.
    This derived class links in member purchases."""

    def __init__(self, group, title, purchaser, recipients, amount, currency, date):
        """Purchase class initialization.

        Keyword arguments:
        group -- group object
        title -- purchase title
        purchaser -- purchaser name
        recipients -- list of recipient names
        amount -- purchase amount
        currency -- purchase currency
        date -- a TimeStamp object
        """
        super().__init__()
        self.group = group
        self.title = title
        self.purchaser = purchaser
        self.recipients = recipients
        self.amount = amount
        self.currency = currency
        self.date = date

        self._link()

    def __del__(self):
        self._unlink()

    def __str__(self):
        return '{:} ({:}) {:}: {:.2f}{:} -> {:}'.format(
            self.title, self.date, self.purchaser.name,
            self._amount, self.currency, ', '.join(self.recipients.keys())
        )

    def _link(self):
        """Link the purchase object in the members objects."""
        members = set(list(self.recipients.values()) + [self.purchaser])
        for member in members:
            member.add_participation(self)

    def _serialize(self):
        """Convert the object to a JSON conform dictionary and return it."""
        return {
            'purchaser': self.purchaser.name,
            'recipients': [x for x in self.recipients],
            'amount': self._amount,
            'currency': self.currency.name,
            'date': str(self.date),
            'title': self.title
        }

    def _unlink(self):
        """Remove the purchase object from the members objects.."""
        members = set(list(self.recipients.values()) + [self.purchaser])
        for member in members:
            member.remove_participation(self)

    @property
    def amount(self):
        return self.group.exchange(self._amount, self.currency)

    @amount.setter
    def amount(self, x):
        self._amount = float(x)

    def get_amount_per_member(self):
        """Calculate the member amount in group currency and return it."""
        return self.amount / self.number_of_recipients

    def is_purchaser(self, name):
        return self.purchaser.name == name

    def is_recipient(self, name):
        return name in self.recipients

    @property
    def number_of_recipients(self):
        """Return the number of recipients."""
        return len(self.recipients.keys())

    @property
    def purchaser(self):
        return self._purchaser

    @purchaser.setter
    def purchaser(self, x):
        self._purchaser = self.group.get_member_by_name(x)

    @property
    def recipients(self):
        return self._recipients

    @recipients.setter
    def recipients(self, x):
        self._recipients = {xx: self.group.get_member_by_name(xx) for xx in x}
