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
# import json
# from .utils import now, BaseException
# from .member import Member
# from .purchase import Purchase
# from .transfer import Transfer
from .stamp import now, encode_datetime, datetime_to_string, decode_datetime


class BaseClass():
    def __init__(self, stamp=now()):
        self.stamp = stamp

    def __repr__(self):
        return '<{:} ({:}) - {:}>'.format(self.__class__.__name__, self.stamp, self)

    def __str__(self):
        return str(self.__dict__)

    def _serialize(self):
        raise(NotImplementedError(self.__class__.__name__))

    def to_dict(self):
        tmp = self._serialize()
        tmp['stamp'] = self.stamp
        return tmp

    @property
    def stamp(self):
        tmp = decode_datetime(self._stamp)
        return datetime_to_string(tmp)

    @stamp.setter
    def stamp(self, x):
        self._stamp = encode_datetime(x)
