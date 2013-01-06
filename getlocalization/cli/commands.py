from getlocalization.cli.opster import command, Dispatcher
from getlocalization.cli.repository import Repository

d = Dispatcher()

@command
def add():
    '''Simple echo program'''
    pass

def main():
    print "Get Localization CLI (C) 2010-2013 Synble Ltd. All rights reserved.\n"
    d.dispatch()
