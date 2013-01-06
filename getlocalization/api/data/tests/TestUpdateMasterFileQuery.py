
import sys,os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

import unittest

from getlocalization.api.data.UpdateMasterFileQuery import UpdateMasterFileQuery

class TestUpdateMasterFileQuery(unittest.TestCase):
    """ generated source for class TestUpdateMasterFileQuery """
    def test(self):
        """ generated source for method test """
        file_ = "testdata/master-file.properties"
        print "Loading test file:" + file_
        query = UpdateMasterFileQuery(file_, "javatestsuite")
        query.setBasicAuth("javatestuser", "asdf1234")
        try:
            query.doQuery()
        except Exception as e:
            self.fail("Exception" + e.getMessage())

if __name__ == '__main__':
    unittest.main()