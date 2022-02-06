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
from .transfer import Transfer


class Balance(Transfer):
    """Balance class derived from transfer class.
    This derived class does not link balance in members."""

    def __init__(self, group, purchaser, recipient, amount, date=now(), currency=None, stamp=now()):
        """Balance class initialization.

        Keyword arguments:
        group -- group object
        purchaser -- purchaser name
        recipient -- recipient name
        amount -- balance amount
        date -- a datetime object, a serialized datetime object or a datetime string (default now())
        currency -- balance currency (default None = group currency)
        stamp -- a datetime object, a serialized datetime object or a datetime string (default now())
        """
        super().__init__(group, purchaser, recipient, amount, date=date,
                         title='balance', description='pending', currency=currency, stamp=stamp)

    def add_transfer(self):
        """Convert the balance object to a transfer object."""
        recipients = list(self.recipients.keys())
        self.group.add_transfer(self.title, self.purchaser.name, recipients,
                                self.amount, date=self.date,
                                description='', currency=self.currency)

    def _link(self):
        """Link the balance object in the members objects."""
        pass

    def _remove_link(self):
        """Remove the balance object from the members objects.."""
        pass
