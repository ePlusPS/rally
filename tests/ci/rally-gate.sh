#!/bin/bash -ex
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# This script is executed by post_test_hook function in desvstack gate.

PROJECT=`echo $ZUUL_PROJECT | cut -d \/ -f 2`
SCENARIO=$BASE/new/$PROJECT/rally-scenarios/${RALLY_SCENARIO}.yaml
PLUGINS_DIR=$BASE/new/$PROJECT/rally-scenarios/plugins
EXTRA_DIR=$BASE/new/$PROJECT/rally-scenarios/extra

RALLY_PLUGINS_DIR=~/.rally/plugins

mkdir -p $RALLY_PLUGINS_DIR
if [ -d $PLUGINS_DIR ]; then
    cp -r $PLUGINS_DIR/*.py $RALLY_PLUGINS_DIR
fi

if [ -d $EXTRA_DIR ]; then
 mkdir -p ~/.rally/extra
 cp -r $EXTRA_DIR/* ~/.rally/extra/
 touch ~/.rally/extra/fake-image.img
fi

env
set -o pipefail

rally use deployment --name devstack
rally deployment check
rally show flavors
rally show images
rally show networks
rally show secgroups
rally show keypairs
rally -v task start --task $SCENARIO

mkdir -p rally-plot/extra
cp $BASE/new/rally/tests/ci/rally-gate/index.html rally-plot/extra/index.html
cp $SCENARIO rally-plot/task.txt
tar -czf rally-plot/plugins.tar.gz -C $RALLY_PLUGINS_DIR .
rally task report --out rally-plot/results.html
gzip -9 rally-plot/results.html
rally task results | python -m json.tool > rally-plot/results.json
gzip -9 rally-plot/results.json
rally task detailed > rally-plot/detailed.txt
gzip -9 rally-plot/detailed.txt
rally task detailed --iterations-data > rally-plot/detailed_with_iterations.txt
gzip -9 rally-plot/detailed_with_iterations.txt
rally task sla_check | tee rally-plot/sla.txt
