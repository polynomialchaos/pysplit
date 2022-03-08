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
from .transfer import Transfer


class Balance(Transfer):
    """Balance class derived from transfer class.
    This derived class does not link balance in members."""

    def __init__(self, group, purchaser, recipient, amount, currency, date):
        """Balance class initialization.

        Keyword arguments:
        group -- group object
        purchaser -- purchaser name
        recipient -- recipient name
        amount -- balance amount
        date -- a TimeStamp object
        """
        super().__init__(group, 'Pending balance',
                         purchaser, recipient, amount, currency, date)

    def to_transfer(self):
        """Convert the balance object to a transfer object."""
        recipients = list(self.recipients.keys())
        self.group.add_transfer(self.title, self.purchaser.name, recipients,
                                self.amount, currency=self.currency, date=self.date)

    def _link(self):
        """Link the balance object in the members objects."""
        pass

    def _unlink(self):
        """Remove the balance object from the members objects.."""
        pass
