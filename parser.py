import argparse

class Parser(object):
    """ Command-line parser """

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Parser')
        self.parser.add_argument('-P', action='store_true', help='equivalent to --partial --progress')
        self.parser.add_argument('-S', action='store_true', help='Handle sparse files efficiently')
        self.parser.add_argument('-a', action='store_true', help='Archive mode')
        self.parser.add_argument('-e', action='store', help='Specify the remote shell to use')
        self.parser.add_argument('-q', action='store_true', help='Decrease verbosity')
        self.parser.add_argument('-v', action='store_true', help='Increase verbosity')
        self.parser.add_argument('-z', action='store_true', help='Compress file data during the transfer')
        self.parser.add_argument('-pass', action='store', dest='passwd', help='Increase verbosity')
        self.parser.add_argument('-progress', action='store_true', help='Increase verbosity')
        self.parser.add_argument('arguments', nargs="*")
        self.args = self.parser.parse_args()
