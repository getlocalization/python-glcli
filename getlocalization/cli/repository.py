import ConfigParser, os

class Repository(object):
    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read(['.gl/repository'])
    
    def create_repository(self):
        self.config.add_section('config')
        self.config.add_section('master_files')
        
        os.makedirs('.gl')
        
        self.commit()
    
    def touch_master(self, local_file):
        mtime = os.path.getmtime(local_file)
        self.config.set("master_files", local_file, str(mtime))
 
   
    def commit(self):
        with open('.gl/repository', 'wb') as configfile:
            self.config.write(configfile)
    
    
    
    
    
    