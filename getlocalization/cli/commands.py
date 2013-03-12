import getpass
import math, os

from getlocalization.cli.opster import command, Dispatcher
from getlocalization.cli.repository import Repository
from getlocalization.api.files.GLMasterFile import GLMasterFile
from getlocalization.api.files.FileFormat import autodetect_fileformat
from getlocalization.api.GLProject import GLProject
from getlocalization.api.files.GLTranslations import GLTranslations

try:
    import simplejson
except:
    import json as simplejson
   
options = [('u', 'username', '', 'Username'),
           ('p', 'password', '', 'Password')]

d = Dispatcher(globaloptions=options)

@d.command(shortlist=True)
def init(projectName, **kwargs):
    '''Create a local repository to working directory and link it to existing Get Localization project.'''
    Repository.create_repository(projectName)
    print "Repository created..."
    
@d.command(shortlist=True)
def add(file, language='en', **kwargs):
    '''Add new master file to project. It will be tracked and pushed when there's changes.'''
    repo = Repository()
    if repo.add_master(file):
        print "File %s added successfully." % repo.relative_path(repo.file_path(file))
    else:
        print "Couldn't find a file %s" % repo.relative_path(repo.file_path(file))
        
    pass
    
@d.command(shortlist=True)
def map_locale(masterFile, languageCode, targetFile, **kwargs):
    '''Map translation of a given master file to local file. When file is pulled from server, it's saved to given target file.'''
    Repository().add_locale_map(masterFile, languageCode, targetFile)
    print "Mapped translation of %s for %s to be saved as %s" % (masterFile, languageCode, targetFile)

@d.command(shortlist=True)
def translations(output=('o', 'human', "Output format e.g. json"), **kwargs):
    '''List translations from given project'''
    repo = Repository();
    
    username = kwargs.get('username')
    password = kwargs.get('password')
    
    if username == '' or password == '':
        username, password = prompt_userpw()
    
    translations = GLTranslations(GLProject(repo.get_project_name(), username, password))
    
    trlist = translations.list()
    
    if output == 'json':
        print simplejson.dumps(trlist)
    else:
        for tr in trlist:
            progress =  str(int(round(float(tr.get('progress'))))) + "%"
            print "#\t%s [%s] %s" % (tr.get('master_file'), tr.get('iana_code'), progress)

@d.command(shortlist=True)
def remote(**kwargs):
    '''Return remote project name'''
    repo = Repository();
    
    print repo.get_project_name()
    
    exit(0)
       
@d.command(shortlist=True)
def pull(**kwargs):
    '''Pull available translations from server'''
    
    repo = Repository();
    
    username = kwargs.get('username')
    password = kwargs.get('password')
  
    if username == '' or password == '':
        username, password = prompt_userpw()
    
    translations = GLTranslations(GLProject(repo.get_project_name(), username, password))
    trlist = translations.list()
    repo.save_status(trlist)
           
    print "#"
                      
    for tr in trlist:
        local_file = repo.get_locale_map(tr.get('master_file'), tr.get('iana_code'))
        if local_file is None:
            print "# Warning: Skipping file %s (%s). Map local file first\n# e.g. with command: gl map-locale %s %s %s.\n# You can also force download files \
to their default locations with parameter --force" % (tr.get('master_file'), tr.get('iana_code'), tr.get('master_file'), tr.get('iana_code'), tr.get('filename'))
            print "#"
            continue
        
        translations.save_translation_file(tr.get('master_file'), tr.get('iana_code'), repo.relative_to_root(local_file))
        
        print "# Translation file %s updated" % local_file
        print "#"
    
    exit(0)

@d.command(shortlist=True)
def push(**kwargs):
    '''Push changed master files to server'''
    
    repo = Repository();
    
    files = repo.get_changed_files()
    
    if len(files) == 0:
        print "#"
        print "# Nothing to push"
        print "#"
        exit(1)
    else:
        print "#\n# Changes not pushed:\n#"
        for file in files:
            print "#\tmodified: %s" % file
        print "#\n"
  
    username = kwargs.get('username')
    password = kwargs.get('password')
  
    if username == '' or password == '':
        username, password = prompt_userpw()
    
    for file in files:
        platformId = autodetect_fileformat(repo.file_path(file))
        
        if platformId is None:
            print "# Couldn't detect file format for file %s, please define it manually" % file
            return
        
        mf = GLMasterFile(GLProject(repo.get_project_name(), username, password), repo.relative_to_root(file), file, platformId)
        mf.push()
        
        repo.touch_master(file)
    
    print "# Done"
    exit(0)
    
@d.command(shortlist=True)
def status(**kwargs):
    '''Project status'''
    repo = Repository()
    
    trlist = repo.get_status()
    
    exit_code = 0
    
    if trlist is not None:
        not_mapped = []
        
        print "# Mapped files:\n#"
        for tr in trlist:
            local_file = repo.get_locale_map(tr.get('master_file'), tr.get('iana_code'))
            
            progress =  str(int(round(float(tr.get('progress'))))) + "%"
            
            if local_file is None:
                not_mapped.append(tr)
            else:
                print "#\t%s [%s] => %s %s" % (tr.get('master_file'), tr.get('iana_code'), local_file, progress)
        
        print "#\n# Files not mapped:\n#"
        for tr in not_mapped:
            print "#\t%s [%s] %s" % (tr.get('master_file'), tr.get('iana_code'), progress)
    else:
        print "#"
        print "# Nothing to report. Pull first to get a proper status."
        print "#"
        exit_code = 1
        
    files = repo.get_changed_files()
    
    if len(files) > 0:
        print "#\n# Changes:\n#"
        for file in files:
            print "# \tmodified: %s" % file
            
    print "#"
    
    exit(exit_code)
    pass

def prompt_userpw():
    print "Get Localization Login"
    username = raw_input('Username (https://www.getlocalization.com):')
    password = getpass.getpass('Password (https://www.getlocalization.com):')
    
    return username, password


def main():
    #print "Get Localization CLI (C) 2010-2013 Synble Ltd. All rights reserved.\n"
    d.dispatch()
