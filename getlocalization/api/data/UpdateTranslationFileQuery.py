
from getlocalization.api.client.Query import Query
from getlocalization.api.client.QuerySecurityException import QuerySecurityException
from getlocalization.api.GLProject import SERVER

class UpdateTranslationFileQuery(Query):
    def __init__(self, file_, projectId, masterFile, languageId):
        super(UpdateTranslationFileQuery, self).__init__()
        self.file_ = file_
        self.projectId = projectId
        self.languageId = languageId
        self.masterFile = masterFile

    def doQuery(self):
        try:
            url = SERVER + self.projectId + "/api/translations/file/" + self.masterFile + "/" + self.languageId + "/";
            self.postFile(self.file_, self.masterFile + "_" + self.languageId, url)
        except QuerySecurityException as cse:
            #  Making sure that URL starts with https.
            cse.printStackTrace()
