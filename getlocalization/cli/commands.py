from getlocalization.cli.opster import command
from getlocalization.cli.repository import Repository


@command
def ca(test,no_newline=('n', False, "don't print a newline")):
    '''Simple echo program'''
    pass

def main():
    dispatch()
