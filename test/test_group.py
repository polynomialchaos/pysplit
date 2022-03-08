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
import json
import os
from pysplit import Group
from pysplit.utils import Currency, TimeStamp


class TestGroup(unittest.TestCase):
    path_1 = "test/res/pysplit.json"
    path_2 = ".pytest_cache/test_group.json"

    def test_group(self):

        # Test: group construction with value
        group = Group("pySplit",
                      "A Python package for money pool split development.", Currency.Euro)
        self.assertTrue(group.turnover == 0.0)
        group.exchange_rates[Currency.USD] = 1.19
        group.set_time("23.06.2021 07:53:55")

        # Test: add members
        member_1 = group.add_member("member_1")
        member_1.set_time("23.06.2021 07:53:55")

        member_2 = group.add_member("member_2")
        member_2.set_time("23.06.2021 07:53:55")

        # Test: add purchases
        purchase = group.add_purchase("purchase_1", "member_1",
                                      ["member_1", "member_2"],
                                      100.0, Currency.Euro, TimeStamp("23.06.2021 07:54:09"))
        purchase.set_time("23.06.2021 07:54:12")

        purchase = group.add_purchase("purchase_2", "member_1",
                                      ["member_2"],
                                      100.0, Currency.Euro, TimeStamp("23.06.2021 07:54:21"))
        purchase.set_time("23.06.2021 07:54:22")

        purchase = group.add_purchase("purchase_3", "member_1",
                                      ["member_1", "member_2"],
                                      200.0, Currency.USD, TimeStamp("23.06.2021 07:57:19"))
        purchase.set_time("23.06.2021 07:57:19")

        # Test: add purchases
        transfer = group.add_transfer("transfer_1", "member_1", "member_1",
                                      200.0, Currency.USD, TimeStamp("23.06.2021 07:57:19"))
        transfer.set_time("23.06.2021 07:57:19")

        # Test: to_dict()
        tmp = group.to_dict()
        self.assertTrue("stamp" in tmp)

        # Test: __str__()
        group()
        print(group)

        # Test: save
        dir_name = os.path.dirname(TestGroup.path_2)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        group.save(TestGroup.path_2)

        # Test: compare
        with open(TestGroup.path_1, 'r') as fp_1:
            json_1 = json.load(fp_1)

            with open(TestGroup.path_2, 'r') as fp_2:
                json_2 = json.load(fp_2)

                self.assertDictEqual(json_1, json_2)


if __name__ == '__main__':

    unittest.main()
