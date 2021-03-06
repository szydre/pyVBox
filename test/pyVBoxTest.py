"""Base class for all pyVBox unittests."""

import os
import os.path
import shutil
import unittest

from pyVBox import HardDisk
from pyVBox import VirtualBox
from pyVBox import VirtualMachine

class pyVBoxTest(unittest.TestCase):
    """Base class for all pyVBox unittests."""
    # VM and HD for testing
    # These are version controlled, we will make a copy before
    # altering them.
    testHDsrc = "test/appliances/TestHD.vdi"
    testHDUUID = "c92b558e-eba5-43e8-a8b3-984f946db1b2"
    testVMsrc = "test/appliances/TestVM.vbox"
    testVMname = "TestVM"

    # Our testing grounds
    testPath = "test/tmp/"
    
    # setUp() will create these copies of the sources above
    testHDpath = "test/tmp/TestHD.vdi"
    testVMpath = "test/tmp/TestVM.xml"

    # Clone we will create during testing
    cloneVMname = "CloneTestVM"
    cloneHDpath = "test/tmp/CloneHD.vdi"

    # Paths for testing failure
    bogusHDpath = "/bogus/path"
    bogusVMpath = "/bogus/path"

    def setUp(self):
        if not os.path.exists(self.testPath):
            os.mkdir(self.testPath)
        shutil.copy(self.testVMsrc, self.testVMpath)
        shutil.copy(self.testHDsrc, self.testHDpath)
        self._cleanup()

    def tearDown(self):
        self._cleanup()

    def _cleanup(self):
        """Unregister test HD and VM if they are registered."""
        # Do machine first to detach any HDs
        try:
            machine = VirtualMachine.find(self.testVMname)
        except:
            pass
        else:
            machine.eject()
        try:
            harddisk = HardDisk.find(self.testHDpath)
        except:
            pass
        else:
            harddisk.close()
        try:
            machine = VirtualMachine.find(self.cloneVMname)
        except Exception as e:
            pass
        else:
            machine.eject()
            machine.delete()
        try:
            clonedisk = HardDisk.find(self.cloneHDpath)
        except:
            pass
        else:
            clonedisk.close()
        try:
            os.remove(self.cloneHDpath)
        except:
            pass
    
def main():
    """Run tests."""
    unittest.main()
