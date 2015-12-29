import random

from script import Script
from line import Line
from character import Character


class StageManager:
    def __init__(self, actors, topics, pool):
        self.characters = self.generateCharacters(actors)
        self.topics = topics
        self.pool = pool
        self.script = Script("TEST SCRIPT")

    def produceScript(self, topic):
        for i in range(1,2):
            for character in self.characters:
                line = Line(random.choice(self.pool), character)
                self.addLine(character, line)
        return self.script

    def generateCharacters(self, actors):
        characters = []
        for ii in range(0, actors):
            name = "Actor " + str(ii+1)
            characters.append(Character(name))
        return characters

    def addLine(self, character, line):
    	character.addLine(line)
    	self.script.addLine(line)



