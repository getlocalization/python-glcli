
import sys,os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from getlocalization.api.data.CreateMasterFileQuery import CreateMasterFileQuery

import unittest

class TestCreateMasterFileQuery(unittest.TestCase):
    """ generated source for class TestCreateMasterFileQuery """
    def test(self):
        """ generated source for method test """
        file_ = "testdata/master-file.properties"
        print "Loading test file:" + file_
        query = CreateMasterFileQuery(file_, "javatestsuite", "javaproperties", "en")
        query.setBasicAuth("javatestuser", "asdf1234")
        try:
            query.doQuery()
        except Exception as e:
            self.fail("Exception" + str(e))


if __name__ == '__main__':
    unittest.main()