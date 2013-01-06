
import sys,os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

import unittest

from getlocalization.api.data.TranslationsQuery import TranslationsQuery

class TestTranslationsQuery(unittest.TestCase):
    """ generated source for class TestTranslationsQuery """
    def test(self):
        """ generated source for method test """
        query = TranslationsQuery("javatestsuite")
        query.setBasicAuth("javatestuser", "asdf1234")
        try:
            query.doQuery()
            print query.getTranslationsZipFile()
        except Exception as e:
            self.fail("Exception" + str(e))

if __name__ == '__main__':
    unittest.main()