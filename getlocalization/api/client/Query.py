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
import urllib2
import base64

from getlocalization.api.client.QuerySecurityException import QuerySecurityException
from getlocalization.api.client.QueryException import QueryException

from multipart_form import MultiPartForm

class Query(object):
    """ generated source for class Query """
    def __init__(self):
        """ generated source for method __init__ """
        self.forcedSSL = False

    def setBasicAuth(self, username, password):
        """ generated source for method setBasicAuth """
        self.forcedSSL = True
        self.username = username
        self.password = password

  
    def postFile(self, file_, pathname, url):
        """ generated source for method postFile """
        if self.forcedSSL and not url.startswith("https"):
            raise QuerySecurityException("SSL is required with basic auth")
        
        request = urllib2.Request(url)
        
        self.set_basicauth(request)
        
        # build form
        fhandle = open(file_)
        form = MultiPartForm()  
    
        print "File: " + file_
        print "Pathname:" + pathname
        
        form.addFile('file', pathname, fhandle)
        form.addField('name', pathname)

        request.add_header("Content-Type", form.getContentType());
        request.add_data(str(form))
        
        try:            
            handle = urllib2.urlopen(request)
            data = handle.read()
            
            if handle.getcode() != 200:
                raise QueryException(data, handle.getcode())
            
            return handle.getcode()
        
        except urllib2.HTTPError, e:
            import traceback
            print traceback.format_exc()
            return -1

        except Exception, e:
            return -1
        
    def getFile(self, url):
        """ generated source for method getFile """
        if self.forcedSSL and not url.startswith("https"):
            raise QuerySecurityException("SSL is required with basic auth")
        
        request = urllib2.Request(url)
        self.set_basicauth(request)

        try:
            handle = urllib2.urlopen(request)
            data = handle.read()
            
            if handle.getcode() != 200:
                raise QueryException(data, handle.getcode())
            
            return data

        except urllib2.HTTPError, e:
            if e.code == 401:
                return False, "Username or password might not be correct."
            
            return False, e.message

    def doQuery(self):
        """ generated source for method doQuery """
        
    def set_basicauth(self, request):
        # basic AUTH set up
        base64string = base64.encodestring('%s:%s' % (self.username, self.password))[:-1]
        authheader =  "Basic %s" % base64string
        request.add_header("Authorization", authheader)

