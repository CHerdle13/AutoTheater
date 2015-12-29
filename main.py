#from script import Script
#from line import Line
#from character import Character
import sys

import get_comments as get_comments
from stageManager import StageManager
import yahoo as yahoo


def main(argv):
    numActors = int(argv[0])
    topics = argv[1:]

    #pool = get_comments.GetCommentPool(topics[0])
    #pool = ["hello"]
    #yahoo.getQuestions(topics[0]);
    #linkCursor = yahoo.database.find({'word': topics[0]})
    #print(linkCursor.count())
    pool = []
    answers = []

    allQuestions = []
    dirtyAnswers = []
    snarkyAnswers = []
    positiveAnswers = []

    questions = yahoo.database.find({'word': topics[0]})

    if questions.count() < 10:
        print("not enough questions")
        yahoo.getQuestions((topics[0]))

    goodQuestions = yahoo.getGoodQuestions('dirtyAnswers', topics[0]).limit(20)
    for quest in goodQuestions:
        allQuestions.append(quest['title'])
        allQuestions.append(quest['question'])
        for a in quest['answers']:
            dirtyAnswers.append(a)
            #print(a['text'])

    goodQuestions = yahoo.getGoodQuestions('snarkyAnswers', topics[0]).limit(20)
    for quest in goodQuestions:
        allQuestions.append(quest['title'])
        allQuestions.append(quest['question'])
        for a in quest['answers']:
            snarkyAnswers.append(a)
            #print(a['text'])

    goodQuestions = yahoo.getGoodQuestions('positiveAnswers', topics[0]).limit(20)
    for quest in goodQuestions:
        allQuestions.append(quest['title'])
        allQuestions.append(quest['question'])
        for a in quest['answers']:
            positiveAnswers.append(a)
            #print(a['text'])




    if(pool.__len__() == 0):
        exit("No results")

    lines = []

    #print("Comment pool:")
    for str in pool:
        if str['type'] == 'question':
            #print(str['text'])
            lines.append(str['text'])
        if str['type'] == 'title':
            #print(str['text'])
            lines.append(str['text'])
        if str['type'] == 'answer':
            lines.append(str['text'])


    manager = StageManager(numActors, topics, lines)
    manager.produceScript(topics)
    manager.script.printScript()

#if __name__ == "__main__": main(sys.argv[1:])
if __name__ == "__main__": main([3, "food"])
