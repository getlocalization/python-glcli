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

from getlocalization.api.data.ListMasterFilesQuery import ListMasterFilesQuery
from getlocalization.api.data.CreateMasterFileQuery import CreateMasterFileQuery
from getlocalization.api.data.UpdateMasterFileQuery import UpdateMasterFileQuery

from getlocalization.api.client.QueryException import QueryException
from getlocalization.api.client.QuerySecurityException import QuerySecurityException
from getlocalization.api.GLException import GLException
from getlocalization.api.GLProject import GLProject

class GLMasterFile(object):
    """ generated source for class GLMasterFile """
    # 
    # 	 * Creates a new <i>GLMasterFile</i> instance by converting the given pathname string into an abstract pathname.
    # 	 * 
    # 	 * @param pathname Path to master file
    # 	 
    def __init__(self, project, pathname, platformId):
        self.myProject = project
        self.platformId = platformId
        self.name = pathname
        self.createdToServer = False

    # 
    # 	 * Returns whether file already exists on server. This will make
    # 	 * a call to server if data is not available.
    # 	 * 
    # 	 * @return true if file already exists on server.
    # 	 * @throws GLException
    # 	 
    def isAvailableRemotely(self):
        """ generated source for method isAvailableRemotely """
        if self.createdToServer:
            return True
        
        query = ListMasterFilesQuery(self.myProject.getProjectName())
        query.setBasicAuth(self.myProject.getUsername(), self.myProject.getPassword())
        
        try:
            query.doQuery()
            
            master_files = query.getMasterFiles()
            
            self.createdToServer = self.name in master_files
            
            return self.createdToServer
        except QueryException as e:
            if e.getStatusCode() == 401:
                raise GLException("Authentication error, please check your username and password" + str(e))
            else:
                raise GLException("Error when processing the query: " + e.getMessage())
        except Exception as e:
            raise GLException("Unable to get information whether master file is available or not: " + str(e))

    # 
    # 	 * Pushes (adds or updates) master file to Get Localization. 
    # 	 * @throws GLException
    # 	 
    def push(self):
        """ generated source for method push """
        if self.isAvailableRemotely():
            self.update()
        else:
            self.add()

    def update(self):
        """ generated source for method update """
        query = UpdateMasterFileQuery(self.getName(), self.myProject.getProjectName())
        query.setBasicAuth(self.myProject.getUsername(), self.myProject.getPassword())
        try:
            query.doQuery()
        except Exception as e:
            raise GLException("Unable to update master file to Get Localization: " + str(e))

    def add(self):
        """ generated source for method add """
        query = CreateMasterFileQuery(self.getName(), self.myProject.getProjectName(), self.platformId, self.myProject.getLanguageId())
        query.setBasicAuth(self.myProject.getUsername(), self.myProject.getPassword())
        try:
            query.doQuery()
        except Exception as e:
            raise GLException("Unable to create master file to Get Localization: " + str(e))

    def getName(self):
        return self.name
