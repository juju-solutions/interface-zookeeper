# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes

class ZookeeperRequires(RelationBase):
    scope = scopes.UNIT

    @hook('{requires:zookeeper}-relation-joined')
    def joined(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.connected')
        conv.remove_state('{relation_name}.departing')


    @hook('{requires:zookeeper}-relation-changed')
    def changed(self):
        conv = self.conversation()
        if self.get_zookeeper_units():
            conv.set_state('{relation_name}.joining')
            conv.set_state('{relation_name}.available')
            

    @hook('{requires:zookeeper}-relation-departed')
    def departed(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.available')
        conv.remove_state('{relation_name}.connected')
        conv.set_state('{relation_name}.departing')


    def dismiss_departing(self):
        for conv in self.conversations():
            conv.remove_state('{relation_name}.departing')


    def dismiss_joining(self):
        for conv in self.conversations():
            conv.remove_state('{relation_name}.joining')


    def get_zookeeper_units(self):
        if not self.conversations():
            raise Exception("Zookeeper private address not set")
            
        units = []        
        for conv in self.conversations():
            units.append((conv.get_remote('private-address'), conv.get_remote('port')))

        return units
