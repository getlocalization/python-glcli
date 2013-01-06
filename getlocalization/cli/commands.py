import getpass

from getlocalization.cli.opster import command, Dispatcher
from getlocalization.cli.repository import Repository
from getlocalization.api.files.GLMasterFile import GLMasterFile
from getlocalization.api.files.FileFormat import autodetect_fileformat
from getlocalization.api.GLProject import GLProject

d = Dispatcher()

@d.command(shortlist=True)
def init(projectName):
    '''Create a local repository to working directory and link it to existing Get Localization project.'''
    Repository().create_repository(projectName)
    print "Repository created..."
    
@d.command(shortlist=True)
def add(file, language='en'):
    '''Add new master file to project. It will be tracked and pushed when there's changes.'''
    Repository().add_master(file)
    pass
    
@d.command(shortlist=True)
def map_locale(masterFile, language, targetFile):
    '''Map translation of a given master file to local file. When file is pulled from server, it's saved to given target file.'''
    pass

@d.command(shortlist=True)
def pull():
    '''Pull available translations from server'''
    pass

@d.command(shortlist=True)
def push():
    '''Push changed master files to server'''
    
    repo = Repository();
    
    files = repo.get_changed_files()
    
    if len(files) == 0:
        print "No changes found\n"
        return
    
    
    username, password = prompt_userpw()
    
    for file in files:
        platformId = autodetect_fileformat(file)
        
        if platformId is None:
            print "Couldn't detect file format for file %s, please define it manually" % file
            return
        
        mf = GLMasterFile(GLProject(repo.get_project_name(), username, password), file, platformId)
        mf.push()
        
        repo.touch_master(file)
    
    pass

@d.command(shortlist=True)
def status():
    '''Project status'''
    
    print autodetect_fileformat('test.properties')
    print autodetect_fileformat('test.strings')
    print autodetect_fileformat('strings.xml')
    print autodetect_fileformat('jorma.po')
    
    pass

def prompt_userpw():
    print "Get Localization Login"
    username = raw_input('Username:')
    password = getpass.getpass()
    
    return username, password

def main():
    print "Get Localization CLI (C) 2010-2013 Synble Ltd. All rights reserved.\n"
    d.dispatch()
