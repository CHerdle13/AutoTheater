class Character:
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.lines = []

    def addLine(self, line):
    	self.lines.append(line)