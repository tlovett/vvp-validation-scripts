# -*- coding: utf8 -*-
# ============LICENSE_START=======================================================
# org.onap.vvp/validation-scripts
# ===================================================================
# Copyright © 2017 AT&T Intellectual Property. All rights reserved.
# ===================================================================
#
# Unless otherwise specified, all software contained herein is licensed
# under the Apache License, Version 2.0 (the "License");
# you may not use this software except in compliance with the License.
# You may obtain a copy of the License at
#
#             http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
#
# Unless otherwise specified, all documentation contained herein is licensed
# under the Creative Commons License, Attribution 4.0 Intl. (the "License");
# you may not use this documentation except in compliance with the License.
# You may obtain a copy of the License at
#
#             https://creativecommons.org/licenses/by/4.0/
#
# Unless required by applicable law or agreed to in writing, documentation
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ============LICENSE_END============================================
#
#

import pytest
from tests import cached_yaml as yaml

from .helpers import validates


@validates("R-901331", "R-481670", "R-663631")
def test_vm_type_assignments_on_nova_servers_only_use_get_param(yaml_file):
    """
    Make sure all nova servers only use get_param for their properties
    """
    with open(yaml_file) as fh:
        yml = yaml.load(fh)

    # skip if resources are not defined
    if "resources" not in yml:
        pytest.skip("No resources specified in the heat template")

    key_values = ["name", "flavor", "image"]
    invalid_nova_servers = set()

    for k, v in yml["resources"].items():
        if not isinstance(v, dict):
            continue
        if "properties" not in v:
            continue
        if "type" not in v:
            continue
        if v["type"] != "OS::Nova::Server":
            continue

        for k2, v2 in v["properties"].items():
            if k2 in key_values:
                if not isinstance(v2, dict):
                    invalid_nova_servers.add(k)
                elif "get_param" not in v2:
                    invalid_nova_servers.add(k)
    msg = (
        "These OS::Nova::Server resources do not derive one or more of "
        + "their {} properties via get_param: {}"
    ).format(", ".join(key_values), ", ".join(invalid_nova_servers))
    assert not invalid_nova_servers, msg
