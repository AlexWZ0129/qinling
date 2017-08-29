# Copyright 2017 Catalyst IT Limited
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import mock

from qinling.tests.unit.api import base

TEST_CASE_NAME = 'TestExecutionController'


class TestExecutionController(base.APITest):
    def setUp(self):
        super(TestExecutionController, self).setUp()

        db_func = self.create_function(prefix=TEST_CASE_NAME)
        self.func_id = db_func.id

    @mock.patch('qinling.rpc.EngineClient.create_execution')
    def test_post(self, mock_create_execution):
        body = {
            'function_id': self.func_id,
        }
        resp = self.app.post_json('/v1/executions', body)

        self.assertEqual(201, resp.status_int)

        resp = self.app.get('/v1/functions/%s' % self.func_id)

        self.assertEqual(1, resp.json.get('count'))

    @mock.patch('qinling.rpc.EngineClient.create_execution')
    def test_get(self, mock_create_execution):
        body = {
            'function_id': self.func_id,
        }
        resp = self.app.post_json('/v1/executions', body)

        self.assertEqual(201, resp.status_int)

        resp = self.app.get('/v1/executions/%s' % resp.json.get('id'))

        self.assertEqual(self.func_id, resp.json.get('function_id'))

    @mock.patch('qinling.rpc.EngineClient.create_execution')
    def test_get_all(self, mock_create_execution):
        body = {
            'function_id': self.func_id,
        }
        resp = self.app.post_json('/v1/executions', body)
        exec_id = resp.json.get('id')

        self.assertEqual(201, resp.status_int)

        resp = self.app.get('/v1/executions')

        self.assertEqual(200, resp.status_int)
        actual = self._assert_single_item(
            resp.json['executions'], id=exec_id
        )
        self._assertDictContainsSubset(actual, body)

    @mock.patch('qinling.rpc.EngineClient.create_execution')
    def test_delete(self, mock_create_execution):
        body = {
            'function_id': self.func_id,
        }
        resp = self.app.post_json('/v1/executions', body)
        exec_id = resp.json.get('id')

        resp = self.app.delete('/v1/executions/%s' % exec_id)

        self.assertEqual(204, resp.status_int)
