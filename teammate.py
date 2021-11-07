
class teammate:
    def __init__(self, parse, type):
        info = parse.split(",")
        if type == 0:
            
            self.char = info[2]
            self.rank = info[3]
        elif type == 1:
            self.char = info[2]
            self.rank = info[1]