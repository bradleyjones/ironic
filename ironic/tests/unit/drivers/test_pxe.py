# Copyright 2015 Hewlett-Packard Development Company, L.P.
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

"""
Test class for PXE Drivers
"""

import mock
import testtools

from ironic.common import exception
from ironic.drivers.modules import ipmitool
from ironic.drivers.modules.irmc import boot as irmc_boot
from ironic.drivers.modules.irmc import management as irmc_management
from ironic.drivers.modules.irmc import power as irmc_power
from ironic.drivers.modules import iscsi_deploy
from ironic.drivers import pxe


class PXEDriversTestCase(testtools.TestCase):

    @mock.patch.object(pxe.importutils, 'try_import', spec_set=True,
                       autospec=True)
    def test_pxe_irmc_driver(self, try_import_mock):
        try_import_mock.return_value = True

        driver = pxe.PXEAndIRMCDriver()

        self.assertIsInstance(driver.power, irmc_power.IRMCPower)
        self.assertIsInstance(driver.console, ipmitool.IPMIShellinaboxConsole)
        self.assertIsInstance(driver.boot, irmc_boot.IRMCPXEBoot)
        self.assertIsInstance(driver.deploy, iscsi_deploy.ISCSIDeploy)
        self.assertIsInstance(driver.management,
                              irmc_management.IRMCManagement)

    @mock.patch.object(pxe.importutils, 'try_import', spec_set=True,
                       autospec=True)
    def test_pxe_irmc_driver_import_error(self, try_import_mock):
        try_import_mock.return_value = False

        self.assertRaises(exception.DriverLoadError,
                          pxe.PXEAndIRMCDriver)
