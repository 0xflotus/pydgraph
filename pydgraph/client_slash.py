# Copyright 2020 Dgraph Labs, Inc.
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

"""Slash GraphQL python client."""
import grpc

import pydgraph
from pydgraph import txn, util, DgraphClientStub
from pydgraph.meta import VERSION
from pydgraph.proto import api_pb2 as api

__author__ = 'Anurag Sharma <anurag@dgraph.io>'
__maintainer__ = 'Arpan Gupta <arpan@dgraph.io>'
__version__ = VERSION
__status__ = 'development'


class SlashGraphQLClient(object):
    """Creates a new Client for interacting with the Slash GraphQL.
    """

    def __init__(self, slash_end_point, api_key):
        if not slash_end_point:
            raise ValueError('No Slash endpoint provided in SlashGraphQLClient constructor')

        self._slash_end_point = slash_end_point
        self._api_key = api_key

    def get_stub(self):
        """Returns Dgraph Client stub for the Slash GraphQL endpoint"""
        url = self._slash_end_point.replace("/graphql", "")
        url = url.replace("https://", "")
        url_parts = url.split(".", 1)
        host = url_parts[0] + ".grpc." + url_parts[1]
        PORT = "443"
        creds = grpc.ssl_channel_credentials()
        call_credentials = grpc.metadata_call_credentials(lambda context, callback: callback((("authorization", self._api_key),), None))
        composite_credentials = grpc.composite_channel_credentials(creds, call_credentials)
        client_stub = pydgraph.DgraphClientStub('{host}:{port}'.format(host=host, port=PORT), composite_credentials, options=(('grpc.enable_http_proxy', 0),))
        return client_stub