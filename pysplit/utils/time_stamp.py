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
import datetime as dt

class TimeStamp():
    """TimeStamp class for storing date and time information.

    Keyword arguments:
    time -- a datetime object or a datetime string (default now())
    """
    fmt_date = r'%d.%m.%Y'
    fmt_time = r'%H:%M:%S'
    fmt_date_time = '{:} {:}'.format(fmt_date, fmt_time)

    def __init__(self, time=None):
        self.time = dt.datetime.now() if time is None else time

    def __str__(self):
        if self._time.time() == dt.time(0, 0):
            return self._time.strftime(TimeStamp.fmt_date)

        return self._time.strftime(TimeStamp.fmt_date_time)

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, x):
        if isinstance(x, dt.datetime):
            self._time = x
        elif isinstance(x, str):
            try:
                self._time = dt.datetime.strptime(x, TimeStamp.fmt_date_time)
            except ValueError:
                self._time = dt.datetime.strptime(x, TimeStamp.fmt_date)
        else:
            raise TypeError("Got unsupported type {:} ({:})!", type(x), [dt.datetime, str])
