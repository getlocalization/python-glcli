
import ConfigParser, os

import os.path

import hashlib
import sys

import json as simplejson

class Repository(object):
    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.optionxform = str
        self.root = self.find_repository()
        
        if self.root is None:
            print "No repository found"
            
            self.root = os.getcwd() + '/'
            
            sys.exit(2)
            
        self.config.read([self.root + '.gl/repository'])
    
    @staticmethod
    def create_repository(projectName):
        config = ConfigParser.ConfigParser()
        config.optionxform = str
        config.add_section('config')
        config.set('config', 'project', projectName)
        
        config.add_section('master_files')
        config.add_section('locale_map')
        config.add_section('status')
        
        try:
            os.makedirs('.gl')
        except:
            pass
        
        root = os.getcwd() + '/'
        
        with open(root + '.gl/repository', 'wb') as configfile:
            config.write(configfile)
    
    def find_repository(self):
        p = os.getcwd()
        
        if os.path.isdir('.gl'):
            return p + '/'
        
        while True:
            tmp = p
            p = os.path.abspath(os.path.join(p, os.pardir))
            
            if os.path.isdir(p + '/.gl'):
                return p + '/'
        
            if tmp == p:
                break
    
   
    def file_path(self, file):
        """
        Get file path for those files that are given from command-line
        """
        
        if file.startswith('/') or file.startswith('\\'):
            return file
        
        return os.path.join(self.root, os.getcwd() + '/' + file)
        
    def relative_path(self, file):
        """
        Return relative path. 
        """
        return os.path.relpath(file, self.root)
    
    def relative_to_root(self, file):
        """
        Get file path for those files that are already processed
        """
        return self.root + "/" + file
    
    def add_master(self, local_file):
        if not os.path.exists(self.file_path(local_file)):
            return False
        
        try:
            if self.config.get("master_files", self.relative_path(self.file_path(local_file))) is not None:
                return True
        except ConfigParser.NoOptionError:
            pass
        
        self.config.set("master_files", self.relative_path(self.file_path(local_file)), str(0))
        self.commit()
        return True
 
    def get_file_hash(self, local_file):
        m = hashlib.md5()
        for line in open(local_file, 'rb'):
            m.update(line)
        return m.hexdigest()
    
    def touch_master(self, local_file):
        #mtime = os.path.getmtime(self.relative_to_root(local_file))
        self.config.set("master_files", self.relative_path(self.relative_to_root(local_file)), self.get_file_hash(self.relative_to_root(local_file)))
        self.commit()
 
    def add_locale_map(self, master_file, languageCode, localFile):
        self.config.set("locale_map", self.relative_path(self.file_path(master_file)) + "/" + languageCode, self.relative_path(localFile))
        self.commit()
    
    def get_mapped_locale(self, master_file, languageCode):
        try:
            return self.config.get("locale_map", master_file + "/" + languageCode)
        except ConfigParser.NoOptionError:
            return None
    
    def parse_locale(self, locale_file):
        idx = locale_file.rfind('/')
        
        return [locale_file[:idx], locale_file[idx+1:]]
        
    def get_locale_map(self):
        return self.config.items("locale_map")
    
    def commit(self):
        with open(self.root + '.gl/repository', 'wb') as configfile:
            self.config.write(configfile)
    
    def get_project_name(self):
        return self.config.get('config', 'project')
    
    def get_changed_files(self):
        files = []
        items = self.config.items('master_files')
        
        for item in items:
            hash = self.get_file_hash(self.relative_to_root(item[0]))
            
            if hash != item[1]:
                files.append(item[0])
                
            #mtime = os.path.getmtime(self.relative_to_root(item[0]))
            
            #if float(mtime) > float(item[1]):
            #    files.append(item[0])
        
        return files
    
    def save_status(self, status):
        self.config.set('status', 'data', simplejson.dumps(status))
        self.commit()
        pass
    
    def get_status(self):
        try:
            return simplejson.loads(self.config.get('status', 'data'))
        except ConfigParser.NoOptionError:
            return None
    
    
    