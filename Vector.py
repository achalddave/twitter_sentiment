"""
This borrows a lot from http://inst.eecs.berkeley.edu/~cs188/fa11/projects/search/docs/util.html
This is currently incomplete. Will add functionality as needed.
"""


class Vector(dict):

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.default = 0

    def __getitem__(self, key):
        if key in self:
            return dict.__getitem__(self, key)
        else:
            return self.default

    def normalize(self):
        total = self.total_value() * 1.0
        normalized = Vector()
        for k in self:
            normalized[k] = self[k]/total
        return normalized

    def total_value(self):
        return sum(self.values())

    def arg_min(self):
        if not self:
            return None
        return sorted(self.items(), key=lambda x: x[1])[0][0]
        
    def arg_max(self):
        if not self:
            return None
        return sorted(self.items(), key=lambda x: -x[1])[0][0]
