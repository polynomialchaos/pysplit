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
from .utils import Base


class Member(Base):
    """Member class derived from pysplit base class."""

    def __init__(self, name):
        """Member class initialization.

        Keyword arguments:
        name -- member name
        """
        super().__init__()
        self.name = name

        self._participations = []

    def __str__(self):
        return self.name

    def _serialize(self):
        """Convert the object to a JSON conform dictionary and return it."""
        return {
            'name': self.name
        }

    def add_participation(self, participation):
        """Add a participation reference to the member.

        Keyword arguments:
        participation -- a participation object reference
        """
        self._participations.append(participation)

    @property
    def balance(self):
        """Calculate the member balance and return the value in groups currency."""
        balance = 0.0
        for participation in self._participations:
            if participation.is_purchaser(self.name):
                balance += participation.amount

            if participation.is_recipient(self.name):
                balance -= participation.get_amount_per_member()

        return balance

    def remove_participation(self, participation):
        """Remove a participation reference from the member.

        Keyword arguments:
        transfer -- a participation object reference
        """
        self._participations.remove(participation)
