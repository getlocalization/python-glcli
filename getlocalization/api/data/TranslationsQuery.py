"""
Copyright (c) 2013, Synble Ltd 
All rights reserved. 

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met: 

    1. Redistributions of source code must retain the above copyright notice, 
       this list of conditions and the following disclaimer. 
     
    2. Redistributions in binary form must reproduce the above copyright 
       notice, this list of conditions and the following disclaimer in the 
       documentation and/or other materials provided with the distribution. 

    3. Neither the name of Synble nor the names of its contributors may be used 
       to endorse or promote products derived from this software without 
       specific prior written permission. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR 
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON 
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. 
"""
from getlocalization.api.client.Query import Query
from getlocalization.api.client.QuerySecurityException import QuerySecurityException
from getlocalization.api.client.QueryException import QueryException

import tempfile, os

class TranslationsQuery(Query):
    """ generated source for class TranslationsQuery """
    # 
    # 	 * Update an existing master file to given Get Localization project. 
    # 	 * 
    # 	 * @param file File that is sent to Get Localization
    # 	 * @param projectId The project name that appears in your Get Localization URL.
    # 	 * 
    # 	 
    def __init__(self, projectId):
        """ generated source for method __init__ """
        super(TranslationsQuery, self).__init__()
        self.projectId = projectId

    def doQuery(self):
        """ generated source for method doQuery """
        try:
            url = "https://www.getlocalization.com/" + self.projectId + "/api/translations/zip";

            data = self.getFile(url);

            tempfd, self.zipFile = tempfile.mkstemp('.zip')
            os.write(tempfd, data)
            os.close(tempfd)
            
        except QuerySecurityException as cse:
            #  Making sure that URL starts with https.
            #cse.printStackTrace()
            raise cse

    def getTranslationsZipFile(self):
        """ generated source for method getTranslationsZipFile """
        return self.zipFile

    