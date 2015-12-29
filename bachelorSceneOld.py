__author__ = 'Curtis'
import yahoo
import redditQA as reddit
import random

from pymongo import Connection, DESCENDING, ASCENDING, MongoClient
global client
client = MongoClient()
global conn
conn = Connection().Bachelor
global question_database
question_database = conn.questions
global comment_database
comment_database = conn.comments

global defaultQuestions
global defaultComments
defaultQuestions = ['When I\'m alone with my dogs I sing songs to them by replacing the important words of songs with the word "dog." What\'s a strange thing that you do when you\'re alone with your pet?',
                    'It seems like my neighbor moved yesterday, but she left her dog tied up outside. What do I do?',
                    'What is your dog\'s name?']
defaultComments = [['I practice my stand-up comedy with my dog. Haven\'t gotten a chuckle out of him yet.',
                   'I have a rabbit and he is stupid. I sometimes put him on my keyboard to see if he\'ll type anything of intelligence; but his fat, fluffy bum just hops across the keys typing nonsense.',
                   'My partner\'s dog is named Banjo, and every now and then I\'ll grab him, roll him onto his back, and "strum" his tummy, while making the banjo noise from Deliverance. He has no idea what the fuck is going on, because he hasn\'t seen Deliverance.',
                   'I yell "Skrillex attack!" then rub my dog\'s belly saying "wubwubwubwubwubwubwub"',
                   'I discuss life problems with my dog, but then I say, "What do you know, Saffy? You\'re a fucking poodle."',
                   'Lol, my dad always sings this made up song to our dog. "DANNY IS A DOG. A DOG DOG DOG. HE DOES DOG THINGS. HE LIVES A DOG\'S LIFE."',
                   'I meow at my cats whenever I see them and continue to have meowing conversations with them.  I do this when people are around, I\'ve stopped caring what other people think, my cats are awesome.',
                   'I call my dog a little fucker.'],
                   ['Congrats on your new pet dog!',
                    'What a mutherfucking sack of shit your neighbor is.'],
                   ['Fido.',
                    'Asshole',
                    'Morty']]

class bachelorActor:
    def __init__(self, number, emotion):
        self.emotion = emotion
        self.number = number

        self.questions = []
        self.responses = []


class BachelorScene:
    def __init__(self, numActors, topics, source, questionCount, skipDownload):
        self.numActors = int(numActors)
        self.topics = topics
        self.source = source
        self.questionCount = questionCount
        self.skipDownload = skipDownload

        self.questions = []
        self.actors = []

        answerTypes = ['questions', 'positive', 'dirty', 'negative',
                       'snarky', 'unique','good']

        i = 0
        while i < numActors:
            self.actors.append(bachelorActor(i+1, answerTypes[i]))
            print("actor " + str(self.actors[i].number) + " has emotion " + self.actors[i].emotion)
            i += 1

        self.getQuestions([topics[0]])
        self.printScript()

    def getQuestions(self, topics):
        for topic in topics:
            if (self.source == "Reddit"):
                if (self.skipDownload):
                    questions = defaultQuestions
                    comments = defaultComments
                else:
                    questions = []
                    comments = []

                    # check number of questions in the database
                    topic_questions = question_database.find({'topic': topic})
                    if topic_questions.count() < (self.questionCount):
                            reddit.getMoreQuestions(topic)
                            topic_questions = question_database.find({'topic': topic})

                    questions = topic_questions
                    comments = comment_database.find({'topic': topic})
                    #for ii in range(0, self.questionCount):

                        #questions.append(reddit.getQuestion(topic))
                        #comments.append(reddit.getComments(questions[ii], topic))
                for ii in range(0, self.questionCount):
                    commentOffset = 0
                    dirtyOffset = 0
                    for actor in self.actors:
                        if (actor.emotion == "questions"):
                            rand_question = random.randint(0, questions.count() - 1)
                            if (self.skipDownload):
                                actor.responses.append(questions[rand_question]['question'])
                            else:
                                actor.responses.append(questions[rand_question]['question'])
                        else:
                            #actor.responses.append(reddit.getDirtyComments(comments[ii])[dirtyOffset])
                            emotion_comments = reddit.getEmotionComments(topic, actor.emotion)
                            for c in emotion_comments:
#                                print(c['text'])
                                actor.responses.append(c['text'])
                        #   dirtyOffset += 1
                        #else:
                        #    actor.responses.append(comments[ii][commentOffset])
                        #   commentOffset += 1
                        #print("\n\nResponses:\n")
                        #print(actor.responses)
            elif (self.source == "Yahoo"):
                questions = yahoo.getQuestions(topic)
                quest = yahoo.getGoodQuestions("numGoodAnswers", topic).limit(1)
                for actor in self.actors:
                    for q in quest:
                        actor.responses.append(q[actor.emotion][0]['text'])
                    print("\n\nResponses:\n")
                    print(actor.responses)

        print("Done")

    def printScript(self):
        print("\n\nSCRIPT:")
        for line in self.printScript():
            print(line)

    def generateScript(self):
        script = []
        for i in range(0, self.questionCount):
            for actor in self.actors:
                if actor.emotion == 'questions':
                    script.append(str(actor.number) + ": " + actor.responses[i])
                else:
                    rand_answer = random.randint(0,len(actor.responses)-1)
                    script.append(str(actor.number) + ": " + actor.responses[rand_answer])
        return script



if __name__ == '__main__':
	scene = BachelorScene(4,['food'],'Reddit', 2, False)


