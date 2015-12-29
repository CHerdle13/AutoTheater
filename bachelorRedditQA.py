import praw
import re
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

global negativeWords
f = open('negative.txt', 'r')
negativeWords = [line.strip() for line in f]
global positiveWords
g = open('positive.txt', 'r')
positiveWords = [line.strip() for line in g]
global verbs
h = open('allVerbs.txt', 'r')
verbs = [line.strip() for line in h]

negativeSet = set(negativeWords)
positiveSet = set(positiveWords)

f.close()
g.close()
h.close()


bad_question_words = ["should I", "can I", "EDIT"]
remove_words = [" of Reddit", "Redditors", "Redditor", "Reddit"]
comment_list = []

global profanity
profanity = (
'sex', 'bum', 'shitfaced', 'fucked', 'plastered', 'wasted', 'hammered', 'cheating', 'sex', 'lust', 'thrust', 'pelvic',
'breast', 'breasts', 'anus', 'arse', 'arsehole', 'ass', 'ass-hat', 'ass-jabber', 'ass-pirate', 'assbag', 'assbandit',
'assbanger', 'assbite', 'assclown', 'asscock', 'asscracker', 'asses', 'assface', 'assfuck', 'assfucker', 'assgoblin',
'asshat', 'asshead', 'asshole', 'asshopper', 'assjacker', 'asslick', 'asslicker', 'assmonkey', 'assmunch', 'assmuncher',
'assnigger', 'asspirate', 'assshit', 'assshole', 'asssucker', 'asswad', 'asswipe', 'axwound', 'bampot', 'bastard',
'beaner', 'bitch', 'bitchass', 'bitches', 'bitchtits', 'bitchy', 'blow job', 'blowjob', 'bollocks', 'bollox', 'boner',
'brotherfucker', 'bullshit', 'bumblefuck', 'butt plug', 'butt-pirate', 'buttfucka', 'buttfucker', 'camel toe',
'carpetmuncher', 'chesticle', 'chinc', 'chink', 'choad', 'chode', 'clit', 'clitface', 'clitfuck', 'clusterfuck', 'cock',
'cockass', 'cockbite', 'cockburger', 'cockface', 'cockfucker', 'cockhead', 'cockjockey', 'cockknoker', 'cockmaster',
'cockmongler', 'cockmongruel', 'cockmonkey', 'cockmuncher', 'cocknose', 'cocknugget', 'cockshit', 'cocksmith',
'cocksmoke', 'cocksmoker', 'cocksniffer', 'cocksucker', 'cockwaffle', 'coochie', 'coochy', 'coon', 'cooter', 'cracker',
'cum', 'cumbubble', 'cumdumpster', 'cumguzzler', 'cumjockey', 'cumslut', 'cumtart', 'cunnie', 'cunnilingus', 'cunt',
'cuntass', 'cuntface', 'cunthole', 'cuntlicker', 'cuntrag', 'cuntslut', 'dago', 'damn', 'deggo', 'dick', 'dick-sneeze',
'dickbag', 'dickbeaters', 'dickface', 'dickfuck', 'dickfucker', 'dickhead', 'dickhole', 'dickjuice', 'dickmilk',
'dickmonger', 'dicks', 'dickslap', 'dicksucker', 'dicksucking', 'dicktickler', 'dickwad', 'dickweasel', 'dickweed',
'dickwod', 'dike', 'dildo', 'dipshit', 'doochbag', 'dookie', 'douche', 'douchebag', 'douchewaffle', 'dumass',
'dumb ass', 'dumbass', 'dumbfuck', 'dumbshit', 'dumshit', 'dyke', 'fag', 'fagbag', 'fagfucker', 'faggit', 'faggot',
'faggotcock', 'fagtard', 'fatass', 'fellatio', 'feltch', 'flamer', 'fuck', 'fuckass', 'fuckbag', 'fuckboy', 'fuckbrain',
'fuckbutt', 'fuckbutter', 'fucked', 'fucker', 'fuckersucker', 'fuckface', 'fuckhead', 'fuckhole', 'fuckin', 'fucking',
'fucknut', 'fucknutt', 'fuckoff', 'fucks', 'fuckstick', 'fucktard', 'fucktart', 'fuckup', 'fuckwad', 'fuckwit',
'fuckwitt', 'fudgepacker', 'gay', 'gayass', 'gaybob', 'gaydo', 'gayfuck', 'gayfuckist', 'gaylord', 'gaytard', 'gaywad',
'goddamn', 'goddamnit', 'gooch', 'gook', 'gringo', 'guido', 'handjob', 'hard on', 'heeb', 'hell', 'ho', 'hoe', 'homo',
'homodumbshit', 'honkey', 'humping', 'jackass', 'jagoff', 'jap', 'jerk off', 'jerkass', 'jigaboo', 'jizz',
'jungle bunny', 'junglebunny', 'kike', 'kooch', 'kootch', 'kraut', 'kunt', 'kyke', 'lardass', 'lesbian', 'lesbo',
'lezzie', 'mcfagget', 'mick', 'minge', 'mothafucka', 'mothafuckin', 'motherfucker', 'motherfucking', 'muff',
'muffdiver', 'munging', 'nigaboo', 'nigga', 'nigger', 'niggers', 'niglet', 'nutsack', 'paki', 'panooch', 'pecker',
'peckerhead', 'penis', 'penisbanger', 'penisfucker', 'penispuffer', 'piss', 'pissed', 'pissflaps', 'polesmoker',
'pollock', 'poon', 'poonani', 'poonany', 'poontang', 'porchmonkey', 'porchmonkey', 'prick', 'punanny', 'punta',
'pussies', 'pussy', 'pussylicking', 'puto', 'queef', 'queer', 'queerbait', 'queerhole', 'renob', 'rimjob', 'ruski',
'sandnigger', 'schlong', 'scrote', 'shit', 'shitass', 'shitbag', 'shitbagger', 'shitbrains', 'shitbreath', 'shitcanned',
'shitcunt', 'shitdick', 'shitface', 'shitfaced', 'shithead', 'shithole', 'shithouse', 'shitspitter', 'shitstain',
'shitter', 'shittiest', 'shitting', 'shitty', 'shiz', 'shiznit', 'skank', 'skeet', 'skullfuck', 'slut', 'slutbag',
'smeg', 'snatch', 'spic', 'spick', 'splooge', 'spook', 'suckass', 'tard', 'testicle', 'thundercunt', 'tit', 'titfuck',
'tits', 'tittyfuck', 'twat', 'twatlips', 'twats', 'twatwaffle', 'unclefucker', 'vag', 'vagina', 'vajayjay', 'vjayjay',
'wank', 'wankjob', 'wetback', 'whore', 'whorebag', 'whoreface', 'wop')
profanitySet = set(profanity)

youSet = ["he", "she", "him"]
yourSet = ["his", "her"]
youreSet = ["he is", "she is", "he's", "she's"]
badPronouns = ["we", "our"] + youreSet + yourSet + youSet

def shorten(comment):
    newcomment = comment
    if "\n" in newcomment:
        newcomment = newcomment.rstrip('\n')
    if newcomment.__len__() > 100:
        periodIndex = newcomment.rfind(".", 0, 100)
        if periodIndex == 0:
            newcomment = newcomment.rstrip(".")
        else:
            newcomment = newcomment[:periodIndex]
    return newcomment

def personalize(comment):
    newComment = comment
    for word in youSet:
        word = " " + word + " "
        newComment = newComment.replace(word, " you ")
    for word in yourSet:
        word = " " + word + " "
        newComment = newComment.replace(word, " your ")
    for word in youreSet:
        word = " " + word + " "
        newComment = newComment.replace(word, " you're ")
    newComment = newComment.replace(" hers ", " yours ")
    newComment = newComment.replace(" us ", " me ")
    newComment = newComment.replace(" we ", " I ")
    newComment = newComment.replace(" our ", " my ")
    newComment = newComment.replace(" ours ", " mine ")
    firstSpace = newComment.find(" ")
    word = newComment[: firstSpace]
    word = word.lower()
    #if word in badPronouns:
    if word in youSet:
        newComment = "You" + newComment[firstSpace:]
    if word in yourSet:
        newComment = "Your" + newComment[firstSpace:]
    if word in youreSet:
        newComment = "You're" + newComment[firstSpace:]
    if "we" in word:
        newComment = "I" + newComment[firstSpace:]
    if "our" in word:
        newComment = "My" + newComment[firstSpace:]


    return newComment

def greeting():
    greetings = ["Hi!", "Hello", "Pleased to meet you.", "G'day mates!", "What's up?", "Nice to meet you.", "How do you do?",
                 "Howdy!", "How are you doing?", "How's it going?", "Hey"]
    intro = ["I have a couple questions for you all today. First: ", "Let's get to know each other a little better. My first question is: ",
             "You all know why you're here, so let's get started: "]
    myGreeting = greetings[random.randint(0,len(greetings)-1)] + " " + intro[random.randint(0,len(intro)-1)]
    return myGreeting


def makeProfane(comment):
    words = comment.split(" ")
    newComment = ""
    for word in words:
        if word in verbs:
            newComment = newComment + " fucking " + word
        else:
            newComment = newComment + " " + word
    choice = random.randint(0,5)
    if choice == 1:
        newComment = newComment + ", bitch"
    elif choice == 2:
        newComment = newComment + ", whoreface"
    elif choice == 3:
        newComment = newComment + ", you fuck"
    elif choice == 4:
        newComment = newComment + ", twatwaffle"
    return newComment

# remove words that shouldn't be in question (basically any variation of 'Reddit'
def removeBadWords(title):
    for word in remove_words:
        title = re.sub(word, '', title, flags=re.I)
    return title

def roastMeResponse():
    user_agent = ("windows:myredditapp:1.0 (by /u/cjw)")
    r = praw.Reddit(user_agent=user_agent)
    submissions = r.search(topic, "AskReddit")



# gives a title of a subreddit a score to rank it
def questionScore(title):
    score = 0 #low score is good
    for bad_word in bad_question_words:
        if bad_word in title:
            score += 2
    for word in remove_words:
        if word in title:
            score += 1
    if title.endswith('?'):
        score -= 1
    if len(title) > 1000:
        score += 5

    return score


#used in ranking (item[0] is score)
def getKey(item):
    return item[0]


#very basic ranking of questions
def rankSubmissions(submissions):
    scoredList = []
    finalList = []
    bestCount = 0
    goodCount = 0
    for sub in submissions:
        score = questionScore(sub.title)
        if score == -1:
            bestCount += 1
        if score == 0:
            goodCount += 1
        addition = (score,sub)
        scoredList.append(addition)
    sortedList = sorted(scoredList, key=getKey)
    for item in sortedList:
        finalList.append(item[1])
    return (finalList, bestCount, goodCount)



#returns all the comments from a subreddit (no replies to comments though)
def getComments(sub, topic):
    print("Getting comments from: " + sub.title + " \nTopic: " + topic)
    sub.replace_more_comments(limit=10, threshold=1) #this takes FOREVER if limit is high
    #flat_comments = praw.helpers.flatten_tree(sub.comments)
    comments = sub.comments
    for comment in comments:
        # check if comments have links (remove these comments)

        new_comment = {}
        new_comment['topic'] = topic
        new_comment['text'] = str(comment.body)
        new_comment['question'] = removeBadWords(sub.title)

        clean = new_comment['text']

        for char in ',;:!?\n\t.\(){}[]':
            clean = clean.replace(char, ' ')
        clean = clean.replace("  ", " ")

        new_comment['tokens'] = clean.split()

        swears = len(profanitySet.intersection(set(comment.body.lower().split(" "))))
        if swears > 2:
            new_comment['dirty'] = True
        else:
            new_comment['dirty'] = False

        if len(positiveSet.intersection(set(new_comment['tokens']))) > 3: #3 is just a guess...
            new_comment['positive'] = True
        else:
            new_comment['positive'] = False

        if len(negativeSet.intersection(set(new_comment['tokens']))) > 3:
            new_comment['negative'] = True
        else:
            new_comment['negative'] = False

        if len(clean) < 12 and len(clean) > 2 and len(profanitySet.intersection(set(new_comment['tokens']))) > 1:
            new_comment['snarky'] = True
        else:
            new_comment['snarky'] = False

        addComment = True


        # other score checks?

        if 'http:' in new_comment['text'] or '[deleted]' in new_comment['text']:
            print("Contained link, did not insert")
        else:
            comment_database.insert(new_comment)
        '''
        try:
            print("Added comment: " + str(comment.body))
        except UnicodeEncodeError:
            print("Couldn't encode this comment.\n")
        '''

    return comment_list
'''
def getDirtyComments(comments):
    # look in database for dirty comments

    dirtyComments = []
    for comment in comments:
        swears = len(profanitySet.intersection(set(comment.lower().split(" "))))
        if swears > 0:
            dirtyComments.append(comment)
    return dirtyComments
'''

def getEmotionComments(topic, emotion, question=None):
    if question == None:
        comments = comment_database.find({'topic': topic, emotion: True})
    else:
        comments = comment_database.find({'question': question, emotion: True})
    if comments.count() < 1:
        if question != None:
            comments = comment_database.find({'question': question})
        else:
            comments = comment_database.find({'topic': topic})
        return comments
    return comments

#returns a subreddit from AskReddit which has to be in question form
#the question is randomly selected as long as it isn't a 'bad' question
def getMoreQuestions(topic):

    user_agent = ("windows:myredditapp:1.0 (by /u/cjw)")
    r = praw.Reddit(user_agent=user_agent)
    submissions = r.search(topic, "AskReddit")
    print("Submissions found: \t" + str(submissions.__sizeof__()))

    rank_output = rankSubmissions(submissions)
    rankedQuestions = rank_output[0]
    num_best_ans = rank_output[1]
    num_good_ans = rank_output[2]
    if num_best_ans >= 1:
        # add to database
        select = random.randint(0,num_best_ans-1)
    elif num_good_ans >= 1:
        # add to database
        select = random.randint(0,num_good_ans-1)
    else:
        # do not add to database
        select = 0

    print("Good questions found: " + str(num_good_ans))
    for ii in range(0, num_good_ans-1):
        new_question = {}
        new_question['topic'] = topic
        new_question['question'] = removeBadWords(rankedQuestions[ii].title)

        getComments(rankedQuestions[ii], topic)

        question_database.insert(new_question)


    #sub = rankedQuestions[select]
    #print(removeBadWords(str(sub.title)))

    # add the question to the MongoDB
    #question_database.insert(sub)
    #return sub


if __name__ == '__main__':
    #c = makeProfane("How are you today")
    c = greeting()
    print(c)
    #question = getMoreQuestions('dogs')
    #getEmotionComments('dogs', 'dirty')
    # print(removeBadWords(question.title) + "\n\n")
    # a = getComments(question, "cats")
    # i = 0
    # if len(a) < 10:
    #     num = len(a)
    # else:
    #     num = 10
    # while i < num:
    #     print(a[i])
    #     i += 1
