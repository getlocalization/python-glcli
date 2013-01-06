import ConfigParser, os
import os.path

class Repository(object):
    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        
        self.root = self.find_repository()
        
        if self.root is None:
            print "No repository found"
            return
            
        self.config.read([self.root + '.gl/repository'])
    
    def find_repository(self):
        p = os.getcwd()
        
        if os.path.isdir('.gl'):
            return p + '/'
        
        while True:
            tmp = p
            p = os.path.abspath(os.path.join(p, os.pardir))
            print p
            
            if os.path.isdir(p + '/.gl'):
                return p + '/'
        
            if tmp == p:
                break
    
    def file_path(self, file):
        return os.path.join(self.root, os.getcwd() + '/' + file)
        
    def relative_path(self, file):
        return os.path.relpath(self.file_path(file), self.root)
    
    def relative_to_root(self, file):
        return self.root + "/" + file
    
    def create_repository(self, projectName):
        self.config.add_section('config')
        self.config.set('config', 'project', projectName)
        
        self.config.add_section('master_files')
        self.config.add_section('locale_map')
        os.makedirs('.gl')
        self.commit()
     
    def add_master(self, local_file):
        if not os.path.exists(self.file_path(local_file)):
            return False
        self.config.set("master_files", self.relative_path(local_file), str(0))
        self.commit()
        return True
 
    def touch_master(self, local_file):
        mtime = os.path.getmtime(self.file_path(local_file))
        self.config.set("master_files", self.relative_path(local_file), str(mtime))
        self.commit()
 
    def add_locale_map(self, master_file, languageCode, localFile):
        self.config.set("locale_map", self.relative_path(master_file) + "/" + languageCode, self.relative_path(localFile))
        self.commit()
    
    def get_locale_map(self, master_file, languageCode):
        try:
            return self.config.get("locale_map", master_file + "/" + languageCode)
        except ConfigParser.NoOptionError:
            return None
    
    def commit(self):
        with open(self.root + '.gl/repository', 'wb') as configfile:
            self.config.write(configfile)
    
    def get_project_name(self):
        return self.config.get('config', 'project')
    
    def get_changed_files(self):
        files = []
        items = self.config.items('master_files')
        
        for item in items:
            mtime = os.path.getmtime(self.file_path(item[0]))
            
            if float(mtime) > float(item[1]):
                print "#\t Modified: %s" % item[0]
                files.append(item[0])
        
        return files
    
    
    
    