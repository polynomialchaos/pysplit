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
import datetime as dt
from dateutil import tz

# tzlocal = dt.timezone.utc
tzlocal = tz.tzlocal()
fmt_local = r'%d.%m.%Y %H:%M:%S'


def encode_datetime(t, timezone=tzlocal, fmt=fmt_local):
    """Encode a datetime object with optional time zone info and format string
    and return a serialized datetime value.

    Keyword arguments:
    t -- a datetime object
    timezone -- a time zone object (default tzlocal)
    fmt -- a format string (default fmt_local)
    """
    if isinstance(t, float):
        return t
    elif isinstance(t, str):
        return encode_datetime(string_to_datetime(t, fmt=fmt), timezone=timezone)

    t.replace(tzinfo=timezone)
    return t.timestamp()


def datetime_to_string(t, fmt=fmt_local):
    """Parse a given datetime object with optional format string
    and return a string.

    Keyword arguments:
    t -- a datetime object
    fmt -- a format string (default fmt_local)
    """
    return t.strftime(fmt)


def decode_datetime(f, timezone=tzlocal):
    """Decode a serialized datetime value with optional time zone info
    and return a datetime object.

    Keyword arguments:
    f -- a serialized datetime value
    timezone -- a time zone object (default tzlocal)
    """
    return dt.datetime.fromtimestamp(f, tz=timezone)


def now(timezone=tzlocal):
    """Return a datetime object from time.time() and optional time zone info.

    Keyword arguments:
    timezone -- a time zone object (default tzlocal)
    """
    return dt.datetime.now(timezone)


def string_to_datetime(s, fmt=fmt_local):
    """Parse a string with optional format string
    and return a datetime object.

    Keyword arguments:
    s -- a string containing date and time
    fmt -- a format string (default fmt_local)
    """
    return dt.datetime.strptime(s, fmt)
