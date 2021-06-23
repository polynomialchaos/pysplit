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
from .purchase import Purchase


class Transfer(Purchase):
    """Transfer class derived from purchase class.
    This derived class links in member transfers."""

    def _link(self):
        """Link the transfer object in the group object."""
        self.purchaser.add_transfer(self)
        for recipient in self.recipients:
            self.recipients[recipient].add_receive(self)

    def _remove_link(self):
        """Remove the transfer object from the group object."""
        self.purchaser.remove_transfer(self)
        for recipient in self.recipients:
            self.recipients[recipient].remove_receive(self)
