# Copyright 2014: One Cloud Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


from rally.benchmark.scenarios import base
from rally.benchmark.scenarios.neutron import utils
from rally.benchmark import validation
from rally import consts

class NetworkScaleTesting(utils.NeutronScenario):

    @validation.required_services(consts.Service.NEUTRON)
    @validation.required_openstack(users=True)
    @base.scenario(context={"cleanup": ["neutron"]})
    def create_tenant_network(self, network_create_args=None, **kwargs):
        """
        Given the network_create_arg, this test will build a
        tenant(multi-tenant) network
        """

        print("network create args: %s, kwargs: %s" % \ 
              (network_create_args, kwargs))
        
        my_context = kwargs["my_context"]

        print("Iteration %s User: %s" % \ 
              (my_context["iteration"],my_context["user"]))
        self._create_network(network_create_args or {})
        self._list_networks


