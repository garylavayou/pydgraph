# Copyright 2023 Dgraph Labs, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests client stub."""

__author__ = 'Garvit Pahal <garvit@dgraph.io>'
__maintainer__ = 'Martin Martinez Rivera <martinmr@dgraph.io>'

import unittest
import sys

import pydgraph
from tests import helper

class TestDgraphClientStub(helper.ClientIntegrationTestCase):
    """Tests client stub."""

    def validate_version_object(self, version):
        tag = version.tag
        if sys.version_info[0] < 3:
            self.assertIsInstance(tag, basestring)
            return

        self.assertIsInstance(tag, str)

    def check_version(self, stub):
        self.validate_version_object(stub.check_version(pydgraph.Check()))

    def test_constructor(self):
        self.check_version(pydgraph.DgraphClientStub(addr=self.TEST_SERVER_ADDR))

    def test_timeout(self):
        with self.assertRaises(Exception):
            pydgraph.DgraphClientStub(self.TEST_SERVER_ADDR).check_version(
                pydgraph.Check(), timeout=-1)

    def test_close(self):
        client_stub = pydgraph.DgraphClientStub(addr=self.TEST_SERVER_ADDR)
        self.check_version(client_stub)
        client_stub.close()
        with self.assertRaises(Exception):
            client_stub.check_version(pydgraph.Check())

class TestFromCloud(unittest.TestCase):
    """Tests the from_cloud function"""
    def test_from_cloud(self):
        testcases = [
            {"endpoint": "godly.grpc.region.aws.cloud.dgraph.io"},
            {"endpoint": "godly.grpc.region.aws.cloud.dgraph.io:443"},
            {"endpoint": "https://godly.region.aws.cloud.dgraph.io/graphql"},
            {"endpoint": "godly.region.aws.cloud.dgraph.io"},
            {"endpoint": "https://godly.region.aws.cloud.dgraph.io"},
            {"endpoint": "godly.region.aws.cloud.dgraph.io:random"},
            {"endpoint": "random:url", "error": True},
            {"endpoint": "google", "error": True},
        ]

        for case in testcases:
            try:
                pydgraph.DgraphClientStub.from_cloud(case["endpoint"], "api-key")
            except IndexError as e:
                if not case["error"]:
                    # we didn't expect an error
                    raise(e)

class TestDgraphClientStubContextManager(helper.ClientIntegrationTestCase):
    def setUp(self):
        pass
    
    def test_context_manager(self):
        with pydgraph.DgraphClientStub(addr=self.TEST_SERVER_ADDR) as client_stub:
            ver = client_stub.check_version(pydgraph.Check())
            self.assertIsNotNone(ver)
    
    def test_context_manager_code_exception(self):
        with self.assertRaises(AttributeError):
            with pydgraph.DgraphClientStub(addr=self.TEST_SERVER_ADDR) as client_stub:
                self.check_version(client_stub) # AttributeError: no such method
                
    def test_context_manager_function_wrapper(self):
        with pydgraph.client_stub(addr=self.TEST_SERVER_ADDR) as client_stub:
            ver = client_stub.check_version(pydgraph.Check())
            self.assertIsNotNone(ver)
    
    
def suite():
    """Returns a test suite object."""
    suite_obj = unittest.TestSuite()
    suite_obj.addTest(TestDgraphClientStub())
    suite_obj.addTest(TestDgraphClientStubContextManager())
    return suite_obj

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
