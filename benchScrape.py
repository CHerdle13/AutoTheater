__author__ = 'Curtis'

import praw
import re
import random

from pymongo import Connection, DESCENDING, ASCENDING, MongoClient
global client
client = MongoClient()
global conn
conn = Connection().Bench
global comments
comments = conn.comments

global negativeWords
f = open('negative.txt', 'r')
negativeWords = [line.strip() for line in f]
global positiveWords
g = open('positive.txt', 'r')
positiveWords = [line.strip() for line in g]

negativeSet = set(negativeWords)
positiveSet = set(positiveWords)

f.close()
g.close()


bad_question_words = ["should I", "can I", "EDIT"]
remove_words = [">", "imgur", "thread", "r/roastme", "r/"]
global pronouns
pronouns = ("i", "me", "us", "my", "our", "we", "his", "her", "he", "she", "i've", "we've", "she's", "he's")
pronounSet = set(pronouns)

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


#---------------------------------------------------------------------------------------------------------------------#
# associate each of these with a score, escalating
physical_features = ('arm', 'bearing', 'build', 'cheekbones', 'cheeks', 'chin',
                     'constitution', 'ears', 'eye-lashes', 'eyebrows',
                     'eyelids', 'eyes', 'face', 'figure', 'fingers',
                     'forehead', 'gait', 'hair', 'hairdo', 'hands', 'jaws', 'legs'
                     'lips', 'marks', 'moustache', 'mouth', 'nose', 'shoulders',
                     'neck', 'short', 'tall', 'teeth',
                     'sex', 'bum', 'breast', 'breasts', 'anus', 'arse', 'arsehole', 'ass', 'asshole', 'boner',
                     'butt', 'camel toe', 'choad', 'chode', 'clit', 'cock', 'cunt', 'dick', 'dildo',
                     'dumb ass', 'fatass', 'pecker', 'penis', 'pussy',
                     'testicle', 'tit', 'tits', 'vag', 'vagina', 'freckles', 'cum', 'throat', 'erect', 'wet' )
phys_dict = {'arm' : 2, 'bearing' : 1, 'build' : 1, 'cheekbones' : 2, 'cheeks' : 2, 'chin' : 3,
                     'constitution' : 1, 'ears' : 3, 'eye-lashes' : 2, 'eyebrows' : 3,
                     'eyelids' : 1, 'eyes' : 3, 'face' : 4, 'figure' : 4, 'fingers' : 2,
                     'forehead' : 4, 'gait' : 1, 'hair' : 2, 'hairdo' : 3, 'hands' : 1, 'jaws' : 3, 'legs' : 1,
                     'lips' : 4, 'marks' : 1, 'moustache' : 3, 'mouth' : 4, 'nose' : 4, 'shoulders' : 2,
                     'neck' : 3, 'short' : 1, 'tall' : 1, 'teeth' : 4,
                     'sex' : 5, 'bum' : 5, 'breast' : 5, 'breasts' : 6, 'anus' : 6, 'arse' : 6, 'arsehole' : 6,
                     'ass' : 3, 'asshole' : 6, 'boner' : 6,
                     'butt' : 5, 'camel toe' : 7, 'choad' : 7, 'chode' : 7, 'clit' : 7, 'cock' : 7, 'cunt' : 7,
                     'dick' : 6, 'dildo' : 5,
                     'dumb ass' : 4, 'fatass' : 4, 'pecker' : 4, 'penis' : 5, 'pussy' : 6,
                     'testicle' : 5, 'tit' : 6, 'tits' : 6, 'vag' : 7, 'vagina' : 6, 'freckles' : 1,
                     'cum' : 5, 'throat' : 4, 'erect' : 6, 'wet' : 6 }

physicalSet = set(physical_features)

social_features = ('friends', 'parents', 'girls', 'guys', 'girlfriend', 'boyfriend','school', 'work', 'siblings',
                   'sister', 'brother', 'mom', 'dad', 'mum')

socialSet = set(social_features)
#---------------------------------------------------------------------------------------------------------------------#



#returns all the comments from a subreddit (no replies to comments though)
def getComments(sub):
    #print("Getting comments from " + sub.title + " \nTopic: " + topic)
    sub.replace_more_comments(limit=None, threshold=0)
    sub_comments = sub.comments
    flat_comments = praw.helpers.flatten_tree(sub_comments)

    added = 0


    #comments = sub.comments
    for comment in flat_comments:
        # check if comments have links (remove these comments)

        new_line = {}
        new_line['text'] = str(comment.body.lower())

        new_line['text'] = new_line['text'].replace(" reddit ", " Earth ")
        new_line['text'] = new_line['text'].replace(" redditors ", " people ")
        new_line['text'] = new_line['text'].replace(" roast ", " insult ")
        new_line['text'] = new_line['text'].replace(" roasted ", " insulted ")
        new_line['text'] = new_line['text'].replace(" roaster ", " jerk ")

        if not("you" in new_line['text']) and not("your" in new_line['text']):
            new_line['text'] = new_line['text'].replace(" he ", " you ")
            new_line['text'] = new_line['text'].replace(" she ", " you ")
            new_line['text'] = new_line['text'].replace(" his ", " your ")
            new_line['text'] = new_line['text'].replace(" hers ", " your ")
            new_line['text'] = new_line['text'].replace(" her ", " your ")
            new_line['text'] = new_line['text'].replace(" he's ", " your're ")
            new_line['text'] = new_line['text'].replace(" she's ", " your're ")

        new_line['submission'] = sub.title
        clean = new_line['text']

        if "edit" in new_line['text']:
            continue

        for char in ',;:!?\n\t.\(){}[]':
            clean = clean.replace(char, ' ')
        clean = clean.replace("  ", " ")

        new_line['tokens'] = clean.split()

        # RANK VULGARITY
        new_line['vulgarity_score'] = 0 # high score is best
        new_line['feature_score'] = 0
        new_line['max_feature'] = ''
        feature_score = 0
        score = 0
        max_score = 10

        if 'http' in new_line['text'] or '[deleted]' in new_line['text']:
            #print("Did not insert")
            continue
        else:
            found = comments.find({'text' : new_line['text']})
            if found.count() > 0:
                continue

        for feature in physicalSet:
            tmp = 0
            if feature in new_line['tokens']:
                tmp = phys_dict[feature]
                if tmp > feature_score:
                    feature_score = tmp
                    new_line['max_feature'] = feature

        new_line['feature_score'] = feature_score

        features = len(physicalSet.intersection(set(comment.body.lower().split(" "))))
        social = len(socialSet.intersection(set(comment.body.lower().split(" "))))

        poor_words = len(set(remove_words).intersection(set(new_line['tokens'])))
        score -= poor_words * 3

        if features + social < 1:
            continue

        #score += social

        #score += features * 2

        swears = len(profanitySet.intersection(set(comment.body.lower().split(" "))))

        new_line['swears'] = swears

        score += (swears * 3)

        negSet = negativeSet.difference(profanitySet)

        #score -= len(positiveSet.intersection(set(new_line['tokens'])))
        score += (1 * len(negSet.intersection(set(new_line['tokens']))))

        num_tokens = len(new_line['tokens'])
        if num_tokens > 20:
            continue
        elif num_tokens < 20 and num_tokens > 4:
            score += 1
        elif num_tokens <= 4:
            score -= 2

        pronouns = len(pronounSet.intersection(set(new_line['tokens'])))
        if pronouns > 1:
            score += 1

        if score > 10:
            score = 10

        new_line['vulgarity_score'] = score

        if score > 0:
            added += 1
            comments.insert(new_line)

        '''
        try:
            print("Added comment: " + new_line['text'] + '\n\tScore: ' +  str(new_line['score']))
        except UnicodeEncodeError:
            print("Couldn't encode this comment.\n")
        '''

    return added

def getMoreComments():

    user_agent = ("windows:myredditapp:1.0 (by /u/cjw)")
    r = praw.Reddit(user_agent=user_agent)
    subreddit = r.get_subreddit("RoastMe")

    allComments = comments.find({})
    num = allComments.count()
    added = 0
    if num < 50:
        print("Getting roasts.")
        # print("Submissions found: \t" + str(subreddit.__sizeof__()))
        for submission in subreddit.get_hot(limit=50):
            '''
            already_scraped = comments.find({'submission': submission.title})
            if already_scraped.count() > 0:
                # skip
                continue
            '''
            #print(submission.title.encode('utf-8'))
            added += getComments(submission)

    if added < 10:
        print("Getting top.")
        for submission in subreddit.get_top_from_month(limit = 20):
            #already_scraped = comments.find({'submission': submission.title})
            '''
            if already_scraped.count() > 0:
                # skip
                continue
            '''
            #print(submission.title.encode('utf-8'))
            getComments(submission)


    '''
    for i in range(1, 11):
        allComments = comments.find({'vulgarity_score' : i})
        print("Found " + str(allComments.count()) + " of score " + str(i))

    allComments = comments.find({'score': 1})
    for c in allComments:
        print(c['text'] + "\n\tScore: " + str(c['score']) + "\n")
    '''

if __name__ == '__main__':
    question = getMoreComments()
