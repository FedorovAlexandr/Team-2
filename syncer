class Syncer(object):
    def __init__(self, targets=None, sources=None, login='user', password='password'):
        self.targets = targets or {}
        self.sources = sources or {}
        self.login = login
        self.password = password
        

    def __setattr__(self, key, value):
        if value == None: return
        if type(value) == 'str':
            self.targets.append(value)
        elif type(value) == 'list' or 'tuple':
            
        self.key = value
    
    def new(self):
        pass

    def add_source(self):    
        pass

    def validate_source(self):
        pass

    def list_sources(self):
        pass

    def add_target(self):
        pass

    def  validate_target(self):
        pass

    def copy(self):
        pass

    def status(self):
        pass

