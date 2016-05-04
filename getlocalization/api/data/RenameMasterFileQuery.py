
from getlocalization.api.client.Query import Query
from getlocalization.api.client.QuerySecurityException import QuerySecurityException
from getlocalization.api.GLProject import SERVER

class RenameMasterFileQuery(Query):
    def __init__(self, projectId, oldFile, newFile):
        super(RenameMasterFileQuery, self).__init__()
        self.projectId = projectId
        self.oldFile = oldFile
        self.newFile = newFile

    def doQuery(self):
        try:
            url = SERVER + self.projectId + "/api/cli-nonpub/rename-master/?component=" + self.oldFile + "&name=" + self.newFile
            data = self.getFile(url)
        except QuerySecurityException as cse:
            #  Making sure that URL starts with https.
            cse.printStackTrace()
