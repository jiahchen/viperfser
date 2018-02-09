
# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import sys
import time
from synchronizers.new_base.SyncInstanceUsingAnsible import SyncInstanceUsingAnsible
from synchronizers.new_base.modelaccessor import *
from xos.logger import Logger, logging

parentdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, parentdir)

logger = Logger(level=logging.INFO)

class SyncVIPSServiceInstance(SyncInstanceUsingAnsible):

    observes = VIPSServiceInstance

    template_name = "viperfserserviceinstance_playbook.yaml"

    service_key_name = "/opt/xos/synchronizers/mcord/mcord_private_key"

    def __init__(self, *args, **kwargs):
        super(SyncVIPSServiceInstance, self).__init__(*args, **kwargs)

    def get_extra_attributes(self, o):
        fields = {}

        return fields

    # To get each network id
    def get_network_id(self, network_name):
        return Network.objects.get(name=network_name).id

    # To get each instance id
    def get_instance_id(self, network_name):
        instances = serviceinstance.objects.all()
        instance_id = instances[0].instance_id
        return instance_id

    def get_ip_address(self, network_name, service_instance, parameter):

        try:
            net_id = self.get_network_id(network_name)
            ins_id = self.get_instance_id(service_instance)
            ip_address = Port.objects.get(network_id=net_id, instance_id=ins_id).ip

        except Exception:
            ip_address = "error"
            print "get failed -- %s" % (parameter)

        return ip_address