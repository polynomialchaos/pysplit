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
from .stamp import Stamp


class Base():
    """Base class for pysplit package.

    Keyword arguments:
    stamp -- a datetime object, a serialized datetime object or a datetime string (default now())
    """

    def __init__(self):
        """Base class initialization.
        """
        self.stamp = Stamp()

    def __repr__(self):
        return '<{:} ({:}) - {:}>'.format(self.__class__.__name__, self.stamp, self)

    def __str__(self):
        return str(self.__dict__)

    def _serialize(self):
        """Convert the object to a JSON conform dictionary and return it.
        Requires implementation in derived class.
        """
        return {}

    def to_dict(self):
        """Convert the object to a JSON conform dictionary.
        This function calls the _serialize method and includes the base class stamp property.
        """
        tmp = self._serialize()
        tmp['stamp'] = str(self.stamp)
        return tmp

    def set_time(self, datetime_or_string):
        self.stamp.time = datetime_or_string
