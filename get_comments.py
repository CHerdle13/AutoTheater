__author__ = 'Curtis'

import praw
import pprint

comment_list = []


def countComments(comments):
    num_comments = 0
    for comment in comments:
        num_comments += 1
        num_comments += countComments(comment.replies)

    return num_comments


def proccessSub(sub):
    sub.replace_more_comments(limit=None, threshold=0)
    total_comments = countComments(sub.comments)
    return total_comments


def getComments(comments):
    for comment in comments:
        comment_list.append(comment.body)
        getComments(comment.replies)

def GetCommentPool(topic):

    user_agent = ("windows:myredditapp:1.0 (by /u/cjw)")

    r = praw.Reddit(user_agent=user_agent)

    reddits = r.search_reddit_names(topic)
    print("Reddits found: \t" + str(reddits.__len__()))

    max_comments = -1
    for x in reddits:
        submissions = r.get_subreddit(x._case_name).get_top_from_year(limit = 2)
        for sub in submissions:
            n_comments = proccessSub(sub)
            if n_comments > max_comments:
                max_comments = n_comments
                my_sub = sub
                my_reddit = x
            my_title = sub.title + "\t" + str(n_comments)
            #print(my_title.encode("utf-8"))

    if max_comments > 0:
        print("\nSubreddit: " + my_reddit._case_name)
        print("Title: " + my_sub.title)
        my_sub.replace_more_comments(limit=None, threshold=0)
        getComments(my_sub.comments)

    return comment_list
