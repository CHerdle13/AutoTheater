__author__ = 'Curtis'

import praw
import re
import random

from pymongo import Connection, DESCENDING, ASCENDING, MongoClient
global client
client = MongoClient()
global conn
conn = Connection().Bench
global complements
comments = conn.complements

#returns all the comments from a subreddit (no replies to comments though)
def getComments(sub):
    #print("Getting comments from " + sub.title)
    #sub.replace_more_comments(limit=None, threshold=0)
    sub_comments = sub.comments
    #flat_comments = praw.helpers.flatten_tree(sub_comments)

    added = 0
    #comments = sub.comments
    for comment in sub_comments:
        # check if comments have links (remove these comments)

        try:

            new_line = {}
            new_line['text'] = str(comment.body.lower())
            new_line['submission'] = sub.title
            clean = new_line['text']

            for char in ',;:!?\n\t.\(){}[]':
                clean = clean.replace(char, ' ')
            clean = clean.replace("  ", " ")

            new_line['tokens'] = clean.split()

            if 'http' in new_line['text'] or '[deleted]' in new_line['text']:
                #print("Did not insert")
                inserted = 0
            else:
                found = comments.find({'text' : new_line['text']})
                if found.count() == 0:
                    if len(new_line['text']) > 60:
                        continue
                    added += 1
                    new_line['text'] = personalize(new_line['text'])
                    comments.insert(new_line)

                '''
                try:
                    print("Added comment: " + new_line['text'] + '\n\tScore: ' +  str(new_line['score']))
                except UnicodeEncodeError:
                    print("Couldn't encode this comment.\n")
                '''
        except AttributeError:
            continue

def getMoreComments():

    user_agent = ("windows:myredditapp:1.0 (by /u/cjw)")
    r = praw.Reddit(user_agent=user_agent)
    subreddit = r.get_subreddit("FreeCompliments")

    allComments = comments.find({})
    num = allComments.count()

    # print("Submissions found: \t" + str(subreddit.__sizeof__()))
    for submission in subreddit.get_hot(limit=20):
        '''
        already_scraped = comments.find({'submission': submission.title})
        if already_scraped.count() > 0:
            # skip
            continue
        '''
        #print(submission.title.encode('utf-8'))
        getComments(submission)


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


if __name__ == '__main__':
    question = getMoreComments()
