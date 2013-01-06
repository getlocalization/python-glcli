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


class GLProject(object):
    """ generated source for class GLProject """
    # 
    # 	 * Creates new GLProject instance with given project name.
    # 	 * 
    # 	 * @param projectName
    # 	 
    def __init__(self, projectName, username, password):
        """ generated source for method __init__ """
        self.projectName = projectName
        self.setUsername(username)
        self.setPassword(password)
        self.setLanguageId("en")

    # 
    # 	 * 
    # 	 * Returns the current language id of master files. 
    # 	 *   
    # 	 * @return IANA formatted language code.
    # 	 
    def getLanguageId(self):
        """ generated source for method getLanguageId """
        return self.languageId

    # 
    # 	 * 
    # 	 * Set the current language id of master files. 
    # 	 *   
    # 	 * @param languageId IANA formatted language code.
    # 	 
    def setLanguageId(self, languageId):
        """ generated source for method setLanguageId """
        self.languageId = languageId

    # 
    # 	 * @return the username
    # 	 
    def getUsername(self):
        """ generated source for method getUsername """
        return self.username

    # 
    # 	 * @param username the username to set
    # 	 
    def setUsername(self, username):
        """ generated source for method setUsername """
        self.username = username

    # 
    # 	 * @return the password
    # 	 
    def getPassword(self):
        """ generated source for method getPassword """
        return self.password

    # 
    # 	 * @param password the password to set
    # 	 
    def setPassword(self, password):
        """ generated source for method setPassword """
        self.password = password

    # 
    # 	 * Returns project name.
    # 	 * 
    # 	 * @return the project name.
    # 	 
    def getProjectName(self):
        """ generated source for method getProjectName """
        return self.projectName

  
