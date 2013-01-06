
from getlocalization.api.client.Query import Query
from getlocalization.api.client.QuerySecurityException import QuerySecurityException

class CreateMasterFileQuery(Query):
    # 
    # 	 * Creates new master file to given Get Localization project. 
    # 	 * 
    # 	 * @param file File that is sent to Get Localization
    # 	 * @param projectId The project name that appears in your Get Localization URL.
    # 	 * @param platformId One of the platforms from supported platform list. http://www.getlocalization.com/library/api/get-localization-file-management-api/
    # 	 * @param languageId Standard IANA language code.
    # 	 * 
    # 	 
    def __init__(self, file_, pathname, projectId, platformId, languageId):
        super(CreateMasterFileQuery, self).__init__()
        self.file_ = file_
        self.projectId = projectId
        self.platformId = platformId
        self.languageId = languageId
        self.pathname = pathname

    def doQuery(self):
        try:
            url = "https://www.getlocalization.com/" + self.projectId + "/api/create-master/" + self.platformId + "/" + self.languageId;
            self.postFile(self.file_, self.pathname, url)
        except QuerySecurityException as cse:
            #  Making sure that URL starts with https.
            cse.printStackTrace()
