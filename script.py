class Script:
    def __init__(self, title):
        self.lines = []
        self.title = title
        
    def addLine(self, line):
        self.lines.append(line)
        
    def addLineAtIndex(self, index, line):
        self.lines.insert(index, line)
        
    def printScript(self):
        print("\n" + self.title)
        for line in self.lines:
            line.printLine()
        print("~fin~\n")