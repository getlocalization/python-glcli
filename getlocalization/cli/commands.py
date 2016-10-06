
import getpass
import math, os, sys
import traceback

from getlocalization.cli.opster import command, Dispatcher
from getlocalization.cli.repository import Repository

from getlocalization.api.files.GLMasterFile import GLMasterFile

from getlocalization.api.files.FileFormat import autodetect_fileformat
from getlocalization.api.GLProject import GLProject
from getlocalization.api.files.GLTranslations import GLTranslations
from getlocalization.api.GLException import GLException

import json as simplejson

options = [('u', 'username', '', 'Username'),
           ('p', 'password', '', 'Password')]

d = Dispatcher(globaloptions=options)

@d.command(shortlist=True)
def init(projectName, **kwargs):
    '''Create a local repository in the working directory and link it to an existing Get Localization project.'''
    Repository.create_repository(projectName)
    print "Repository created..."
    
@d.command(shortlist=True)
def add(file, language='en', **kwargs):
    '''Add a new master file to project. It will be tracked and pushed when there are changes.'''
    repo = Repository()
    if repo.add_master(file):
        print "File %s added successfully." % repo.relative_path(repo.file_path(file))
    else:
        print "Couldn't find a file %s" % repo.relative_path(repo.file_path(file))

@d.command(shortlist=True)
def remove(file, language='en', **kwargs):
    '''Remove master file from a remote project. This will remove the master file (and related translations). Local file is not removed.'''
    repo = Repository()

    if repo.master_exists(file):
        username = kwargs.get('username')
        password = kwargs.get('password')
      
        if username == '' or password == '':
            username, password = prompt_userpw()
       
        mf = GLMasterFile(GLProject(repo.get_project_name(), username, password), repo.relative_to_root(file), file, None)
        
        try:
            mf.remove()
            repo.rm_master(file)
            print "File %s removed successfully." % repo.relative_path(repo.file_path(file))
        except GLException as e:
            print "Unable to remove file from server: " + str(e)
    else:
        print "Couldn't find a file %s" % repo.relative_path(repo.file_path(file))

@d.command(shortlist=True)
def map_locale(masterFile, languageCode, targetFile, **kwargs):
    '''Map translation of given master file to a local file. When the file is pulled from server, it's saved in the given target file.'''
    Repository().add_locale_map(masterFile, languageCode, targetFile)
    print "Mapped translation of %s for %s to be saved as %s" % (masterFile, languageCode, targetFile)

@d.command(shortlist=True)
def map_master(oldFile, newFile, **kwargs):
    '''Map existing master file on server to new a location on your local repository. This also changes the filename on server-side to match your local directory structure.'''
    
    repo = Repository()

    username = kwargs.get('username')
    password = kwargs.get('password')
  
    if username == '' or password == '':
        username, password = prompt_userpw()


    mf = GLMasterFile(GLProject(repo.get_project_name(), username, password), repo.relative_to_root(oldFile), repo.relative_path(repo.file_path(oldFile)), None)

    if not mf.isAvailableRemotely():
        print "Error: File " + oldFile + " is not available on the server."
        return

    try:
        if repo.rename_master_file(oldFile, newFile):
            mf.rename(newFile, repo.relative_path(repo.file_path(newFile)))
            repo.commit() # Commit the rename to local repo after successful request to server

            translations = GLTranslations(GLProject(repo.get_project_name(), username, password))
            trlist = translations.list()
            repo.save_status(trlist)

            print "Successfully mapped master %s => %s" % (oldFile, newFile)
        else:
            print "Error when mapping master file."
    except EnvironmentError as err:
        print err


@d.command(shortlist=True)
def translations(output=('o', 'human', "Output format e.g. json"), **kwargs):
    '''List translations from current project'''
    repo = Repository();
    
    username = kwargs.get('username')
    password = kwargs.get('password')
    
    if username == '' or password == '':
        username, password = prompt_userpw()
    
    translations = GLTranslations(GLProject(repo.get_project_name(), username, password))
    
    try:
        trlist = translations.list()
    
        if output == 'json':
            print simplejson.dumps(trlist)
        else:
            for tr in trlist:
                progress =  str(int(round(float(tr.get('progress'))))) + "%"
                print "#\t%s [%s] %s" % (tr.get('master_file'), tr.get('iana_code'), progress)
    except:
        print "# Project is empty"

@d.command(shortlist=True)
def remote(**kwargs):
    '''Return remote project name'''
    repo = Repository();
    
    print repo.get_project_name()
    
    sys.exit(0)


@d.command(shortlist=True)
def pull(**kwargs):
    '''Pull available translations from server'''
    
    repo = Repository();
    
    username = kwargs.get('username')
    password = kwargs.get('password')
  
    if username == '' or password == '':
        username, password = prompt_userpw()
    
    exitVal = 0
    try:
        translations = GLTranslations(GLProject(repo.get_project_name(), username, password))
        trlist = translations.list()
        repo.save_status(trlist)
               
        print "#"
                          
        for tr in trlist:
            local_file = repo.get_mapped_locale(tr.get('master_file'), tr.get('iana_code'))
            if local_file is None:
                print "# Warning: Skipping file %s (%s). Map local file first\n# e.g. with command: gl map-locale %s %s %s.\n# You can also force download files \
    to their default locations with parameter --force" % (tr.get('master_file'), tr.get('iana_code'), tr.get('master_file'), tr.get('iana_code'), tr.get('filename'))
                print "#"
                continue
            
            translations.save_translation_file(tr.get('master_file'), tr.get('iana_code'), repo.relative_to_root(local_file))
            
            print "# Translation file %s updated" % local_file
            print "#"
    except:
        print traceback.format_exc()
        print "#"
        print "# Project is empty"
        print "#"
        exitVal = 1
        
    sys.exit(exitVal)

@d.command(shortlist=True)
def push(**kwargs):
    '''Push changed master files to server'''
    
    repo = Repository();
    
    files = repo.get_changed_files()
    
    if len(files) == 0:
        print "#"
        print "# Nothing to push"
        print "#"
        sys.exit(1)
    else:
        print "#\n# Changes not pushed:\n#"
        for file in files:
            print "#\tmodified: %s" % file
        print "#\n"
  
    username = kwargs.get('username')
    password = kwargs.get('password')
  
    if username == '' or password == '':
        username, password = prompt_userpw()
    
    error = False

    for file in files:
        platformId = autodetect_fileformat(repo.file_path(file))
        
        if platformId is None:
            print "# Couldn't detect file format for file %s, please define it manually" % file
            return
        
        mf = GLMasterFile(GLProject(repo.get_project_name(), username, password), repo.relative_to_root(file), file, platformId)

        try:
            mf.push()
            repo.touch_master(file)
        except GLException as e:
            error = True
            print e.message
        
    if not error:
        print "# Done"
    sys.exit(0)

@d.command(shortlist=True)
def push_tr(force=('f', False, 'also push files existing on server'), **kwargs):
    '''Push local mapped translations that don't exist on server'''
    repo = Repository();
    username = kwargs.get('username')
    password = kwargs.get('password')
  
    if username == '' or password == '':
        username, password = prompt_userpw()
        
    push_translations(repo, username, password, force)

def push_translations(repo, username, password, force):
    # Push translations that don't exist
    translations = GLTranslations(GLProject(repo.get_project_name(), username, password))
    
    try:
        trlist = translations.list()
    except:
        pass
      
    locale_map = repo.get_locale_map()   
    for locale in locale_map:
        tr_file = repo.parse_locale(locale[0])
        local_file = locale[1]
        
        found = False
        for tr in trlist:
            if tr.get('master_file') == tr_file[0] and tr.get('iana_code') == tr_file[1]:
                found = True
        
        if force or not found:
            try:
                translations.update_translation_file(local_file, tr_file[0], tr_file[1])
            except:
                #traceback.print_exc()
                print "# Updating file '" + local_file + "' failed"
        else:
            print "#"
            print "# File already exists on server-side, use --force to force push it"
            print "#"
        
 
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
            local_file = repo.get_mapped_locale(tr.get('master_file'), tr.get('iana_code'))
            
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
    
    sys.exit(exit_code)
    pass

def prompt_userpw():
    print "Get Localization Login"
    username = raw_input('Username (https://www.getlocalization.com):')
    password = getpass.getpass('Password (https://www.getlocalization.com):')
    
    return username, password


def main():
    #print "Get Localization CLI (C) 2010-2013 Synble Ltd. All rights reserved.\n"
    d.dispatch()
    
