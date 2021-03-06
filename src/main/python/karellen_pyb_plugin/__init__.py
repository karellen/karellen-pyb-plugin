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

import textwrap

from pybuilder.core import use_plugin, init, task, before

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.distutils")
use_plugin("python.pycharm")
use_plugin("python.cram")
use_plugin("python.sphinx")
use_plugin("pypi:pybuilder_header_plugin")


@init
def configure(project):
    project.build_depends_on("wheel", "~=0.29.0")
    project.build_depends_on("coverage", "~=4.2")
    project.build_depends_on("sphinx", "~=1.5.0.dev")
    project.build_depends_on("sphinx_rtd_theme", ">=0.0.1")

    # Integration Test Configuration
    project.set_property("dir_source_integrationtest_python", "src/integrationtest/python")
    project.set_property("integrationtest_module_glob", "*_tests")
    project.set_property("integrationtest_test_method_prefix", None)
    project.set_property("integrationtest_runner", project.get_property("unittest_runner"))

    # Unit test Coverage Configuration
    project.set_property("unittest_coverage_threshold_warn", 100)
    project.set_property("unittest_coverage_branch_threshold_warn", 100)
    project.set_property("unittest_coverage_branch_partial_threshold_warn", 100)
    project.set_property("unittest_coverage_break_build", True)
    project.set_property("unittest_coverage_exceptions", [])

    # Integration Test Coverage Configuration
    project.set_property("integrationtest_coverage_threshold_warn", 100)
    project.set_property("integrationtest_coverage_branch_threshold_warn", 100)
    project.set_property("integrationtest_coverage_branch_partial_threshold_warn", 100)
    project.set_property("integrationtest_coverage_break_build", True)
    project.set_property("integrationtest_coverage_exceptions", [])

    # Flake8 Configuration
    project.set_property("flake8_break_build", True)
    project.set_property("flake8_include_test_sources", True)
    project.set_property("flake8_include_scripts", True)
    project.set_property("flake8_exclude_patterns", ".svn,CVS,.bzr,.hg,.git,__pycache__,*.sh")

    # Copyright Header
    project.set_property("pybuilder_header_plugin_break_build", True)
    project.set_property("pybuilder_header_plugin_expected_header",
                         textwrap.dedent("""\
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
                         """))
    project.set_property("pybuilder_header_plugin_exclude_patterns", [])

    # Cram Configuration
    project.set_property("cram_fail_if_no_tests", True)

    # Distutils
    project.set_property("distutils_classifiers", ["Development Status :: 5 - Production/Stable",
                                                   "Environment :: Console",
                                                   "Intended Audience :: Developers",
                                                   "License :: OSI Approved :: Apache Software License",
                                                   "Programming Language :: Python",
                                                   "Programming Language :: Python :: 3.5"
                                                   ]
                         )
    project.set_property("distutils_commands", ["sdist", "bdist_wheel"])
    project.set_property("distutils_upload_sign", True)
    project.set_property("distutils_upload_sign_identity", "5F4AFAA3")
    project.set_property("distutils_readme_description", True)
    project.set_property("distutils_description_overwrite", True)

    # Sphinx
    project.set_property("sphinx_output_per_builder", True)
    project.set_property("sphinx_run_apidoc", True)
    project.set_property("sphinx_apidoc_extra_args", ["-l", "-e"])
    project.set_property("sphinx_build_extra_args", ["-E"])


@task
def run_integration_tests(project, logger):
    from pybuilder.plugins.python import unittest_plugin

    unittest_plugin.run_tests(project, logger, "integrationtest", "integration tests")


@before("sphinx_generate_documentation")
def set_sphinx_html_path(project):
    import sphinx_rtd_theme

    sphinx_conf = project.get_property("sphinx_project_conf")
    sphinx_conf["html_theme"] = "sphinx_rtd_theme"
    sphinx_conf["html_theme_path"] = [sphinx_rtd_theme.get_html_theme_path()]

    # Napoleon settings
    sphinx_conf["extensions"].append("sphinx.ext.napoleon")
    sphinx_conf["napoleon_google_docstring"] = True
    sphinx_conf["napoleon_numpy_docstring"] = False
    sphinx_conf["napoleon_include_init_with_doc"] = False
    sphinx_conf["napoleon_include_private_with_doc"] = False
    sphinx_conf["napoleon_include_special_with_doc"] = False
    sphinx_conf["napoleon_use_admonition_for_examples"] = False
    sphinx_conf["napoleon_use_admonition_for_notes"] = False
    sphinx_conf["napoleon_use_admonition_for_references"] = False
    sphinx_conf["napoleon_use_ivar"] = False
    sphinx_conf["napoleon_use_param"] = True
    sphinx_conf["napoleon_use_rtype"] = True
    sphinx_conf["napoleon_use_keyword"] = True


@before("verify")
def run_coverage(project, logger, reactor):
    from pybuilder.plugins.python import coverage_plugin

    execution_manager = reactor.execution_manager
    if execution_manager.is_task_in_current_execution_plan("run_unit_tests"):
        coverage_plugin.run_coverage(project, logger, reactor, "unittest_coverage", "unit test coverage",
                                     "run_unit_tests", shortest_plan=True)
    if execution_manager.is_task_in_current_execution_plan("run_integration_tests"):
        coverage_plugin.run_coverage(project, logger, reactor, "integrationtest_coverage", "integration test coverage",
                                     "run_integration_tests", shortest_plan=True)


@before("verify")
def run_header_check(project, logger, reactor):
    reactor.execute_task_shortest_plan("check_source_file_headers")
