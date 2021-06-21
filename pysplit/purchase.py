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


class Purchase():
    def __init__(self, purchaser, recipients, amount, name='', description='', stamp=now()):
        self.purchaser = purchaser
        self.recipients = recipients
        self.amount = amount
        self.name = name
        self.description = description
        self.stamp = stamp

        self._linkMembers()

    @property
    def amount_pp(self):
        return self.amount / len(self.recipients)

    @property
    def recipients(self):
        return self._recipients

    @recipients.setter
    def recipients(self, recipients):
        self._recipients = recipients if isinstance(
            recipients, list) else [recipients]

    def _serialize(self):
        keys = ['amount', 'name', 'description', 'stamp']
        tmp = {key: getattr(self, key) for key in keys}
        tmp.update({'purchaser': self.purchaser.name})
        tmp.update({'recipients': [x.name for x in self.recipients]})
        return tmp

    def _linkMembers(self):
        self.purchaser.addPurchase(self)
        for recipient in self.recipients:
            recipient.addReceive(self)

    def _remove(self):
        self.purchaser._remove(self)
        for recipient in self.recipients:
            recipient._remove(self)

    def __str__(self):
        str_info = '{:} - '.format(self.name) if self.name else ''
        str_info += '{:} - '.format(self.description) if self.description else ''
        str_info += '{:}: {:} -> {:}'.format(
            self.purchaser.name, self.amount, ', '.join([x.name for x in self.recipients]))
        return str_info

    def __repr__(self):
        return '<{:} ({:}) - {:}>'.format(self.__class__.__name__, self.stamp, self)
