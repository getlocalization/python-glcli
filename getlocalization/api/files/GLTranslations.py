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

from getlocalization.api.data import CreateMasterFileQuery, ListMasterFilesQuery, TranslationsQuery, UpdateMasterFileQuery
from getlocalization.api.client.QueryException import QueryException
from getlocalization.api.client.QuerySecurityException import QuerySecurityException
from getlocalization.api.GLException import GLException
from getlocalization.api.GLProject import GLProject

import zipfile

class GLTranslations(object):
    """ generated source for class GLTranslations """
    # 
    # 	 * Creates a new <i>GLTranslations</i> instance.
    # 	 * 
    # 	 * @param project Project you're downloading translations from.
    # 	 
    def __init__(self, project):
        """ generated source for method __init__ """
        self.myProject = project

    # 
    # 	 * Pull the translations from server to target directory. Note that request
    # 	 * may take some time as translated files are generated on the server-side and
    # 	 * depending of the load it's possible but unlikely that call immediately throws 
    # 	 * GLServerBusyException which means you should try again in a moment.
    # 	 * 
    # 	 * @param targetDirectory
    # 	 * @throws GLException, GLServerBusyException
    # 	 
    def pull(self, targetDirectory):
        """ generated source for method pull """
        query = TranslationsQuery(self.myProject.getProjectName())
        query.setBasicAuth(self.myProject.getUsername(), self.myProject.getPassword())
        try:
            query.doQuery()
            zipFile = query.getTranslationsZipFile()
            self.unzip(zipFile, targetDirectory)
        except Exception as e:
            e.printStackTrace()
            raise GLException("Unable to download translations: " + str(e))

    # 
    # 	 * Pull the translations from server to target directory but don't unzip them. Note that request
    # 	 * may take some time as translated files are generated on the server-side and
    # 	 * depending of the load it's possible but unlikely that call immediately throws 
    # 	 * GLServerBusyException which means you should try again in a moment.
    # 	 * 
    # 	 * @param targetDirectory
    # 	 * @throws GLException, GLServerBusyException
    # 	 
    def pull_0(self):
        """ generated source for method pull_0 """
        query = TranslationsQuery(self.myProject.getProjectName())
        query.setBasicAuth(self.myProject.getUsername(), self.myProject.getPassword())
        try:
            query.doQuery()
            return query.getTranslationsZipFile()
        
        except QueryException as e:
            if e.getStatusCode() == 401:
                raise GLException("Authentication error, please check your username and password" + str(e))
            else:
                raise GLException("Error when processing the query: " + str(e))
        except Exception as e:
            e.printStackTrace()
            raise GLException("Unable to download translations: " + str(e))

    def unzip(self, zip, target):
        zipf = zipfile.ZipFile(zip)
        zipf.extractall(path=target)