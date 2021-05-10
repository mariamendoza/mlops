import argparse

class ArgParser():

    def __init__(self, description=None):
        self.description = description

    def build_parser(self):
        self.parser = argparse.ArgumentParser(description=self.description)
        
    def add_argument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)    
    
    def parse_args(self):
        self.args = self.parser.parse_args()
        return self.args
        
__all__ = ("ArgParser")