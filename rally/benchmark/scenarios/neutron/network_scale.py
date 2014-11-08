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
import pprint

from rally.benchmark.scenarios import base
from rally.benchmark.scenarios.neutron import utils
from rally.benchmark import validation
from rally import consts

class TestState(object):
    """
    Represents a base State for Load Scenario Testing 
    """
    
    def __init__(self,name):
        """
        constructor
        """
        self._name = name
    
    def __str__(self):
        """string representation of a TestState"""
        return self._name
    
    def execute(self,state_context, args):
        """ virtual execute method """
        #assert (0,"execute not implemented")
        pass
    
    def next(self, event):
        # assert (0,"next not implemented")
        pass

class ExternalNetworkCreate(TestState):
    """
    Scale Test expects to create an External Network
    """
    def __init__(self):
        super(ExternalNetworkCreate,self).__init__(name="ExternalNetworkCreate")

    """
    Represents the test execution state of creating
    an external network
    """
    def execute(self, state_context, args):
        print("creating external networks")
    
        tenant = args["tenant"]

        if (tenant == "tenant-a"):
            #  transition to the next state
            print("transitioning to the next state")
            state_context.current_state = StateContext.InternalNetworkCreate
        else:
            pass

class InternalNetworkCreate(TestState):
    """
    Represents the test execution state for
    creating internal networks
    """
    
    def __init__(self):
        super(InternalNetworkCreate,self).__init__(name="InternalNetworkCreate")

    def execute(self, state_context, args):
        print("creating internal networks")

        if (True):
            print("transitioning to the next state")
            state_context.current_state = StateContext.DoneState
            
class DoneState(TestState):
    
    def __init__(self):
        super(DoneState, self).__init__(name="DoneState")
    
    def execute(self, state_context, args):
        print("done")

class StateContext:
    def __init__(self, initial_state):
        self.current_state = initial_state
    
    def execute(self, args):
        assert (self.current_state != None)
        self.current_state.execute(self,args)

# define static attributes
StateContext.ExternalNetworkCreate = ExternalNetworkCreate()
StateContext.InternalNetworkCreate = InternalNetworkCreate()
StateContext.DoneState = DoneState()

"""
A dictionary keyed by tenant-ids
{'tenant-1':{
                     'current-test-state':stateContextObj
                     'network' : {"net-1": ... }
                     }
         'tenant-2':{
                     'current-test-state':stateContextObj2
                    }
        }
         
"""
class NetworkScaleTesting(utils.NeutronScenario):

    @validation.required_services(consts.Service.NEUTRON)
    @validation.required_openstack(users=True)
    @base.scenario(context={"cleanup": ["neutron"]})
    def create_tenant_network(self, network_create_args=None, **kwargs):
        """
        Given the network_create_arg, this test will build a
        tenant(multi-tenant) network
        
        This test scenario will build the multi-tenant network in the following
        order

        external-network
        internal-network
        hosts
        """
       
        # begin-debug-kwargs / context print out
        print("****************************************")
        print("network create args: %s,\n" %
              (network_create_args))
        print("kwargs:")         
        pprint.pprint(kwargs)
        
        my_context = kwargs["my_context"]

        print("Iteration %s\n" %
              (my_context["iteration"]))
        
        print("user:")
        pprint.pprint(my_context["user"])
        print("****************************************")
        # end-debug-kwargs / context print out

        self._create_network(network_create_args or {})
        self._list_networks


