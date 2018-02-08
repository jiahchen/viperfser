
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


from synchronizers.new_base.modelaccessor import *
from synchronizers.new_base.model_policies.model_policy_tenantwithcontainer import TenantWithContainerPolicy

class VIPSServiceInstancePolicy(TenantWithContainerPolicy):
    model_name = "VIPSServiceInstance"

    def handle_create(self, service_instance):
        return self.handle_update(service_instance)

    def handle_update(self, service_instance):
        if (service_instance.link_deleted_count>0) and (not service_instance.provided_links.exists()):
            self.logger.info("The last provided link has been deleted -- self-destructing.")
            self.handle_delete(service_instance)
            if VIPSServiceInstance.objects.filter(id=service_instance.id).exists():
                service_instance.delete()
            else:
                self.logger.info("Tenant %s is already deleted" % service_instance)
            return

        self.manage_container(service_instance)

    def handle_delete(self, service_instance):
        if service_instance.instance and (not service_instance.instance.deleted):
            all_service_instances_this_instance = VIPSServiceInstance.objects.filter(instance_id=service_instance.instance.id)
            other_service_instances_this_instance = [x for x in all_service_instances_this_instance if x.id != service_instance.id]
            if (not other_service_instances_this_instance):
                self.logger.info("VIPSServiceInstance Instance %s is now unused -- deleting" % service_instance.instance)
                service_instance.instance.delete()
            else:
                self.logger.info("VIPSServiceInstance Instance %s has %d other service instances attached" % (service_instance.instance, len(other_service_instances_this_instance)))
