__author__ = 'Curtis'
import sys
import yahoo
import bachelorRedditQA as reddit
import random
import bachelorInsultsScrape as bench
import bachelorComplementsScrape as comp

from pymongo import Connection, DESCENDING, ASCENDING, MongoClient
global client
client = MongoClient()
global conn
conn = Connection().Bachelor
global question_database
question_database = conn.questions
global comment_database
comment_database = conn.comments
global insults
insults = conn.insults
global complements
complements = conn.complements

global usedQuestions
usedQuestions = []

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
        self.source = source.capitalize()
        self.questionCount = questionCount
        self.skipDownload = skipDownload

        self.questions = []
        self.actors = []

        self.escalation = int(10/self.questionCount)

        answerTypes = ['positive', 'dirty', 'negative',
                       'snarky', 'unique','good']

        # i = 0
        # while i < numActors:
        #     self.actors.append(bachelorActor(i+1, answerTypes[i]))
        #     print("actor " + str(self.actors[i].number) + " has emotion " + self.actors[i].emotion)
        #     i += 1
        if self.numActors < 3:
            raise AttributeError("This game needs at least 3 actors.")
            print("This game needs at least 3 actors")
            sys.exit(0)
        bachelor = bachelorActor(1,'questions')
        self.actors.append(bachelor)
        print("actor 1 is the bachelor(ette)")
        for i in range(2,numActors):
            rand_emotion = random.randint(0,5)
            self.actors.append(bachelorActor(i,answerTypes[rand_emotion]))
            print("actor " + str(self.actors[i-1].number) + " has emotion " + self.actors[i-1].emotion)
        self.actors.append(bachelorActor(numActors, 'bitch'))
        print("actor " + str(numActors) + " is kind of a bitch")



        self.getQuestions(self.topics)
        bachelor = self.actors[0]
        if len(bachelor.responses) == 0:
            bachelor.responses.append("")
        bachelor.responses[0] = reddit.greeting() + bachelor.responses[0]
        self.bachelorResponses()
        self.printScript()

    def bachelorResponses(self):
        self.getCompliments()
        usedCompliments = []
        length = len(self.actors[0].responses)
        for x in range(1,length):
            all_compliments = complements.find({})
            compliments_count = all_compliments.count()
            # for com in all_compliments:
            #     try:
            #         print(com['text'])
            #     except:
            #         continue
            rand_compliment = random.randint(0, compliments_count-1)
            while rand_compliment in usedCompliments:
                rand_compliment = random.randint(0, compliments_count-1)
            #myCompliment = str(all_compliments[rand_compliment]['text']) #--------DON'T KNOW WHY THIS DOESN'T WORK :(
            myCompliment = "Great answers!"
            self.actors[0].responses[x] = myCompliment + " " + self.actors[0].responses[x]
            usedCompliments.append(rand_compliment)
        self.actors[0].responses.append("Well, I never! You certainly have guts. I like guts. Marry me?")
        #return bachelor


    def getInsults(self, more=False):
        found_insults = insults.find({})

        if found_insults.count() < 100 or more:
            bench.getMoreComments()

    def getCompliments(self):
        found_compliments = complements.find({})
        if found_compliments.count() < 100:
            comp.getMoreComments()

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

                    questions = []
                    for i in range(0, topic_questions.count()):
                        questions.append(topic_questions[i]['question'])
                    #comments = comment_database.find({'topic': topic})
                    #for ii in range(0, self.questionCount):

                        #questions.append(reddit.getQuestion(topic))
                        #comments.append(reddit.getComments(questions[ii], topic))
                for ii in range(0, self.questionCount):
                    commentOffset = 0
                    dirtyOffset = 0
                    usedResponses = []
                    bitch_used = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[]}
                    prev_score = -1
                    for actor in self.actors:
                        if (actor.emotion == "questions"):
                            rand_num = random.randint(0, len(questions) - 1)
                            rand_question = questions[rand_num]
                            check_comments = comment_database.find({'question': rand_question})
                            num_comments = check_comments.count()

                            while num_comments < self.numActors - 2:
                                if rand_num in usedQuestions:
                                    continue
                                usedQuestions.append(rand_num)
                                rand_num = random.randint(0, len(questions) - 1)
                                check_comments = comment_database.find({'question': rand_question})
                                num_comments = check_comments.count()
                                if len(usedQuestions) > len(questions) - self.questionCount:
                                    return(["Sorry, not enough data for topic was found. Please try less questions or another topic."])
                                    print("Sorry, not enough data for topic was found. Please try less questions or another topic.")
                                    sys.exit(1)
                            while rand_num in usedQuestions: # won't work if number of subreddits found is less than number of questions asked for
                                rand_num = random.randint(0, len(questions) - 1)
                            usedQuestions.append(rand_num)
                            #rand_question = questions[rand_num]['question']

                            if (self.skipDownload):
                                actor.responses.append(rand_question)
                            else:
                                actor.responses.append(reddit.personalize(rand_question))
                        elif actor.emotion == "bitch":
                            self.getInsults()
                            score = (ii+1)*self.escalation
                            bitch_responses = insults.find({'score': score})
                            count = bitch_responses.count()
                            rand_line = random.randint(0,count-1)
                            while count == 0:
                                score = score - 1
                                bitch_responses = insults.find({'score': score})
                                count = bitch_responses.count()
                                if score == -1:
                                    userInput = raw_input("No more insults found. Press 'Y' to find more, press 'N' to quit \n")
                                    s = str(userInput)
                                    if s == "y" or s == "Y":
                                       self.getInsults(True)
                                       score = (ii+1)*self.escalation
                                    else:
                                        print("Bye")
                                        sys.exit(0)
                                elif score == prev_score:
                                    if count == bitch_used[score].count():
                                        userInput = raw_input("Not enough insults for escalation. Find more? (Y/N) \n")
                                        s = str(userInput)
                                        if s == "y" or s == "Y":
                                            self.getInsults(True)
                                            score = (ii+1)*self.escalation

                            if count > 0:
                                prev_score = score
                                while rand_line in bitch_used[score]:
                                    rand_line = random.randint(0,count-1)
                                bitch_used[score].append(rand_line)
                                newline = reddit.shorten(bitch_responses[rand_line]['text'])
                                actor.responses.append(reddit.personalize(newline))
                            else:
                                print("No bitchy comments found")
                        elif actor.emotion == "Bachelor_response":
                            all_complements = complements.find({})
                            complements_count = all_complements.count()
                            rand_complement = random.randint(0, complements_count-1)
                            actor.responses.append(all_complements[rand_complement]['text'])
                        else:
                            #actor.responses.append(reddit.getDirtyComments(comments[ii])[dirtyOffset])
                            emotion_comments = reddit.getEmotionComments(topic, actor.emotion, rand_question)
                            if emotion_comments.count() < self.numActors - 2:
                                emotion_comments = comment_database.find({'question': rand_question})
                            rand_response = random.randint(0, emotion_comments.count() - 1)
                            while rand_response in usedResponses:
                                rand_response = random.randint(0, emotion_comments.count() - 1)
                            usedResponses.append(rand_response)
                            actor.responses.append(reddit.shorten(emotion_comments[rand_response]['text']))
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

    def generateScript(self):
        script = []
        for i in range(0, self.questionCount):
            for actor in self.actors:
                # pick a random response from actor.responses
                if actor.emotion == 'questions':
                    script.append(str(actor.number) + ": " + actor.responses[i])
                else:
                    #rand_answer = random.randint(0,len(actor.responses)-1)
                    script.append(str(actor.number) + ": " + actor.responses[i])
        script.append("1: " + self.actors[0].responses[self.questionCount])
        return script

    def printScript(self):
        print("\n\nSCRIPT:")
        for line in self.generateScript():
            print(line)

def main():
    scene = BachelorScene(3,['pizza'],'Reddit', 2, False)
    scene.printScript()

if __name__ == '__main__':
    main()


