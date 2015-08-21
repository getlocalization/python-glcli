Get Localization CLI
============

## Getting started ##

<pre>sudo pip install gl</pre>

<small>Prerequisite is that you have Python 2.x (and pip) installed on your computer. This is typically already available on Mac OS X and Linux machines, however for Windows you may have to install it from <a href="https://www.python.org/downloads/windows/">Python website</a>. For Windows you should also drop the "sudo" command as it's not needed, simply install it with command <i>pip install gl</i></small>

## Basics ##

With Get Localization CLI you can push and pull translation files. 

<pre>
usage: gl <command> [options]

commands:

 add           Add a new master file to project. It will be tracked and pushed when there are changes.
 init          Create a local repository in the working directory and link it to an existing Get Localization project.
 map-locale    Map translation of given master file to a local file. When the file is pulled from server, it's saved in the given target file.
 pull          Pull available translations from server
 push          Push changed master files to server
 push-tr       Push local mapped translations that don't exist on server
 remote        Return remote project name
 remove        Remove master file from project.
 status        Project status
 translations  List translations from current project
</pre>

## Init project ##
<pre>
$ gl init [project-name]
Repository created...
</pre>

project-name  Project name should match with your project name on Get Localization server: https://www.getlocalization.com/[project-name]/
 
Creates a Get Localization repository to the current directory. Repository meta-data is saved in .gl folder. This can be added to your version control (git, hg, svn etc). If you need a different configuration for different branches, it's possible.

## Adding files ##

<pre>
$ gl add master/English.properties
File master/English.properties added successfully.
</pre>

'add' command is for adding a *master* file to repository. I.e. a file that will translated.

## Mapping locales ##

Instead of adding translated files, you can map a local file to the translation on the server. This is done with gl map-locale command:

<pre>
gl map-locale [master-filename] [language-IANA-code] [translation-filename-in-local-filesystem]
</pre>

Note that translation-filename-in-local-filesystem doesn't need to actually exist in the file system. If it does, see push-tr command as well. 

Example:

<pre>
$ gl map-locale master/English.properties fi locale/Finnish.properties
Mapped translation of master/English.properties for fi to be saved as locale/Finnish.properties
</pre>

When you run gl pull, the file that contains Finnish translations (IANA code: fi) of master/English.properties file is saved to locale/Finnish.properties file.

## Push ##

<pre>
$ gl push
</pre>

push command sends all altered *master* files to the Get Localization server for translation.

## Pull ##

<pre>
$ gl pull
</pre>

pull command fetches all updated translation files from Get Localization server. Note that only mapped locales will be downloaded and stored. If you use --force the default location will be used.

## Pushing translations (Use with caution) ##

<pre>
gl push-tr
</pre>

push-tr command is meant for pushing existing translations to the Get Localization server. Typically you only want to do this once (when you start your project and you have translations in local files that don't yet exist on server). After project start translations are managed by the Get Localization server so pushing translation from local machine is not necessary or even recommended. In order for this to work, you need to map locales (see 'Mapping Locales' and map-locale command). 

### Working with git, mercurial (hg) and other version management systems

It's recommended to add gl configuration files to your version management system. You can simply add the .gl directory that is created under the directory where you executed the gl init command. Configuration files do not contain any usernames or passwords, only the information about the repository (e.g. mapped translation files and master files)

