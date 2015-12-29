__author__ = 'Curtis'

import praw
import re
import random

from pymongo import Connection, DESCENDING, ASCENDING, MongoClient
global client
client = MongoClient()
global conn
conn = Connection().Bachelor
global complements
complements = conn.complements

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
            x = str(comment.body)
        except:
            continue
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
                found = complements.find({'text' : new_line['text']})
                if found.count() == 0:
                    added += 1
                    complements.insert(new_line)

                '''
                try:
                    print("Added comment: " + new_line['text'] + '\n\tScore: ' +  str(new_line['score']))
                except UnicodeEncodeError:
                    print("Couldn't encode this comment.\n")
                '''
        except AttributeError:
            continue
        except:
            continue

def getMoreComments():

    user_agent = ("windows:myredditapp:1.0 (by /u/cjw)")
    r = praw.Reddit(user_agent=user_agent)
    subreddit = r.get_subreddit("FreeCompliments")

    allComments = complements.find({})
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


if __name__ == '__main__':
    question = getMoreComments()
