import ConfigParser, os

class Repository(object):
    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read(['.gl/repository'])
    
    def create_repository(self, projectName):
        self.config.add_section('config')
        self.config.set('config', 'project', projectName)
        self.config.add_section('master_files')
        os.makedirs('.gl')
        self.commit()
     
    def add_master(self, local_file):
        self.config.set("master_files", local_file, str(0))
        self.commit()
 
    def touch_master(self, local_file):
        mtime = os.path.getmtime(local_file)
        self.config.set("master_files", local_file, str(mtime))
        self.commit()
 
    def commit(self):
        with open('.gl/repository', 'wb') as configfile:
            self.config.write(configfile)
    
    def get_project_name(self):
        return self.config.get('config', 'project')
    
    def get_changed_files(self):
        files = []
        items = self.config.items('master_files')
        
        for item in items:
            mtime = os.path.getmtime(item[0])
            
            if float(mtime) > float(item[1]):
                print "Modified: %s" % item[0]
                files.append(item[0])
        
        return files
    
    
    
    