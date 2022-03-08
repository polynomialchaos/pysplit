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
import unittest
from datetime import datetime
from pysplit.utils import at_least_1d, Base, TimeStamp


class TestUtils(unittest.TestCase):
    date_string = "23.02.2022"
    date_time_string = "{:} 00:30:00".format(date_string)

    def test_base(self):
        # Test: construction
        base = Base()

        # Test: set the time
        base.set_time(datetime.now())
        base.set_time(TestUtils.date_time_string)
        base.set_time(TestUtils.date_string)

        # Test: to_dict()
        tmp = base.to_dict()
        self.assertTrue("stamp" in tmp)

        # Test: __str__()
        print(base)

    def test_stamp(self):
        # Test: overload construction
        now = datetime.now()

        stamp_1 = TimeStamp()
        stamp_2 = TimeStamp(now)
        stamp_3 = TimeStamp(TestUtils.date_time_string)

        # Test: set short date string
        print(stamp_1)
        stamp_1.time = TestUtils.date_string
        print(stamp_1)

        # Test: get time object
        self.assertTrue(stamp_2.time == now)

        # Test: toString()
        self.assertTrue(TestUtils.date_string == stamp_1.__str__())
        self.assertTrue(TestUtils.date_time_string == stamp_3.__str__())

        # Test: raise DateTimeParseException
        self.assertRaises(ValueError, stamp_2.__setattr__, "time", "01.02.22")
        self.assertRaises(TypeError, stamp_2.__setattr__, "time", 1)

    def test_utils(self):
        # Test: at_least_1d
        value = 2.0
        tmp = at_least_1d(value)
        tmp = at_least_1d(value)
        self.assertListEqual([value], tmp)


if __name__ == '__main__':

    unittest.main()
