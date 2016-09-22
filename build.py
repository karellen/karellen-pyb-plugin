#
#  -*- coding: utf-8 -*-
#
# (C) Copyright 2016 Karellen, Inc. (http://karellen.co/)
#
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
#

import sys

sys.path.insert(0, "src/main/python")

from pybuilder.core import init, use_plugin, Author

use_plugin("python.core")
use_plugin("karellen_pyb_plugin")

name = "karellen-pyb-plugin"
version = "0.0.1.dev"

url = "https://github.com/karellen/karellen-pyb-plugin"
summary = "Karellen PyBuilder Plugin"
description = "Please visit %s for more information!" % url

authors = [Author("Karellen, Inc", "supervisor@karellen.co")]
default_task = ["install_dependencies", "analyze", "publish"]
license = "Apache License, Version 2.0"


@init
def set_properties(project):
    # Coverage Configuration
    project.set_property("unittest_coverage_threshold_warn", 0)
    project.set_property("unittest_coverage_branch_threshold_warn", 0)
    project.set_property("unittest_coverage_branch_partial_threshold_warn", 0)
    project.set_property("integrationtest_coverage_threshold_warn", 0)
    project.set_property("integrationtest_coverage_branch_threshold_warn", 0)
    project.set_property("integrationtest_coverage_branch_partial_threshold_warn", 0)

    # Cram Configuration
    project.set_property("cram_fail_if_no_tests", False)

    # PDoc
    project.set_property("pdoc_module_name", "karellen_pyb_plugin")
