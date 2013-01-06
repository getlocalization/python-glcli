
import sys,os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from getlocalization.api.data.ListMasterFilesQuery import ListMasterFilesQuery

import unittest

class TestListMasterFilesQuery(unittest.TestCase):
    """ generated source for class TestListMasterFilesQuery """
    def test(self):
        """ generated source for method test """
        query = ListMasterFilesQuery("javatestsuite")
        query.setBasicAuth("javatestuser", "asdf1234")
        try:
            query.doQuery()
            master_files = query.getMasterFiles()
            
            if "master-file.properties" not in master_files:
                self.fail("Cannot find master-file.properties from project")
            
        except Exception as e:
            self.fail("Exception" + str(e))

if __name__ == '__main__':
    unittest.main()