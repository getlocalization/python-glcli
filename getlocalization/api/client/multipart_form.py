"""
Copyright (c) 2011-2013, Synble Ltd 
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
import itertools
import mimetools
import mimetypes

class MultiPartForm(object):
    """Accumulate the data to be used when posting a form."""

    def __init__(self):
        self.formFields = []
        self.files = []
        self.boundary = mimetools.choose_boundary()

    def getContentType(self):
        return 'multipart/form-data; boundary=%s' % self.boundary

    def addField(self, name, value):
        """Add a form field to the form data."""
        self.formFields.append((name, value))

    def addFile(self, fieldname, filename, fileHandle, mimetype=None):
        body = fileHandle.read()
        if mimetype is None:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'

        self.files.append((fieldname, filename, mimetype, body))

    def __str__(self):
        parts = []
        partBoundary = '--' + self.boundary

        # Add the form fields

        parts.extend([ partBoundary,'Content-Disposition: form-data; name="%s"' % name,
        '', value,] for name, value in self.formFields)

        # Add the files to upload
        # Amazon S3 expects file data to be 'Content-Disposition:
        # form-data' instead of "file"

        parts.extend([ partBoundary,'Content-Disposition: form-data; name="%s"; filename="%s"' % \
        (fieldName, filename),'Content-Type: %s' % contentType,'',body,]
        for fieldName, filename, contentType, body in self.files)

        # Flatten the list and add closing boundary marker,
        # then return \r\n separated data
        flattened = list(itertools.chain(*parts))
        flattened.append('--' + self.boundary + '--')
        flattened.append('')
        return '\r\n'.join(flattened)