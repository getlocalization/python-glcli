import getpass

from getlocalization.cli.opster import command, Dispatcher
from getlocalization.cli.repository import Repository
from getlocalization.api.files.GLMasterFile import GLMasterFile
from getlocalization.api.files.FileFormat import autodetect_fileformat
from getlocalization.api.GLProject import GLProject
from getlocalization.api.files.GLTranslations import GLTranslations

d = Dispatcher()

@d.command(shortlist=True)
def init(projectName):
    '''Create a local repository to working directory and link it to existing Get Localization project.'''
    Repository().create_repository(projectName)
    print "Repository created..."
    
@d.command(shortlist=True)
def add(file, language='en'):
    '''Add new master file to project. It will be tracked and pushed when there's changes.'''
    repo = Repository()
    if repo.add_master(file):
        print "File %s added successfully." % repo.relative_path(file)
    else:
        print "Couldn't find a file %s" % repo.relative_path(file)
        
    pass
    
@d.command(shortlist=True)
def map_locale(masterFile, languageCode, targetFile):
    '''Map translation of a given master file to local file. When file is pulled from server, it's saved to given target file.'''
    Repository().add_locale_map(masterFile, languageCode, targetFile)
    print "Mapped translation of %s for %s to be saved as %s" % (masterFile, languageCode, targetFile)
     
@d.command(shortlist=True)
def pull():
    '''Pull available translations from server'''
    
    repo = Repository();
    
    username, password = prompt_userpw()
    
    translations = GLTranslations(GLProject(repo.get_project_name(), username, password))
    trlist = translations.list()
                             
    for tr in trlist:
        local_file = repo.get_locale_map(tr.get('master_file'), tr.get('iana_code'))
        if local_file is None:
            print "Warning: Skipping file %s (%s). Map local file first e.g. with command: gl map-locale %s %s %s. You can also force download files \
to their default locations with parameter --force" % (tr.get('master_file'), tr.get('iana_code'), tr.get('master_file'), tr.get('iana_code'), tr.get('filename'))
            continue
        
        translations.save_translation_file(tr.get('master_file'), tr.get('iana_code'), repo.relative_to_root(local_file))
        
        print "Translation file %s updated" % local_file
    
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
        print file
        platformId = autodetect_fileformat(repo.file_path(file))
        
        if platformId is None:
            print "Couldn't detect file format for file %s, please define it manually" % file
            return
        
        print repo.file_path(file)
        mf = GLMasterFile(GLProject(repo.get_project_name(), username, password), repo.file_path(file), file, platformId)
        mf.push()
        
        repo.touch_master(file)
    
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
    username = raw_input('Username (https://www.getlocalization.com):')
    password = getpass.getpass('Password (https://www.getlocalization.com):')
    
    return username, password

def main():
    #print "Get Localization CLI (C) 2010-2013 Synble Ltd. All rights reserved.\n"
    d.dispatch()
