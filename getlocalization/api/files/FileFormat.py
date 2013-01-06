
import os

FORMATS = [['.po', 'gettext'],
           ['.properties', 'javaproperties'],
           ['.ini', 'ini'],
           ['.json', 'json'],
           ['.resx', 'resx'],
           ['.xliff', 'xliff'],
           ['.ts', 'qt'],
           ['.xliff', 'xliff'],
           ['.js', 'js'],
           ['.php', 'phparray'],
           ['.docx', 'docx'],
           ['.txt', 'plain'],
           ['.strings', 'ios']
          ]

def autodetect_fileformat(filename):
    fileName, fileExt = os.path.splitext(filename)
    
    if fileName == 'strings' and fileExt == '.xml':
        return 'android'
    
    for format in FORMATS:
        if format[0] == fileExt:
            return format[1]
        
    
    