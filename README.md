Get Localization CLI
============

## Getting started ##

<pre>sudo pip install gl</pre>

## Basics ##

With Get Localization CLI you can push and pull translation files. 

<pre>
usage: gl <command> [options]

commands:

 add           Add new master file to project. It will be tracked and pushed when there's changes.
 init          Create a local repository to working directory and link it to existing Get Localization project.
 map-locale    Map translation of a given master file to local file. When file is pulled from server, it's saved to given target file.
 pull          Pull available translations from server
 push          Push changed master files to server
 push-tr       Push local mapped translations that do not exist on server
 remote        Return remote project name
 status        Project status
 translations  List translations from given project
</pre>

## Init project ##
<pre>
$ gl init [project-name]
Repository created...
</pre>

project-name  project name should match with your project name on Get Localization server: https://www.getlocalization.com/[project-name]/
 
Creates Get Localization repository to current directory. Repository meta-data is saved under .gl folder. This can be added to your version control (git, hg, svn etc). If you need different configuration for different branches, it's possible.

## Adding files ##

<pre>
$ gl add master/English.properties
File master/English.properties added successfully.
</pre>

'add' command is for adding *master* file to repository. I.e. the file that will translated.

## Mapping locales ##

Instead of adding translated files, you can map the local file to the server translation. This happens with gl map-locale command:

<pre>
gl map-locale [master-filename] [language-IANA-code] [translation-filename-in-local-filesystem]
</pre>

Note that translation-filename-in-local-filesystem doesn't need to exist actually in file system. If it does, see push-tr command as well. 

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

push command sends all the altered *master* files to Get Localization server for translation.

## Pull ##

<pre>
$ gl pull
</pre>

pull command fetches all the updated translation files from Get Localization server. Note that only mapped locales will be downloaded and stored. If you use --force the default location will be used.

## Pushing translations (Use with caution) ##

<pre>
gl push-tr
</pre>

push-tr command is meant for pushing existing translations to Get Localization server. Typically you want to do this only once (when you init your project and you have translations in local files that don't yet exist on server). After this translations are managed by Get Localization server so pushing translation from local machine is not necessary or even recommended. In order to this work, you need to map locales (see 'Mapping Locales' and map-locale command). 

