__author__ = 'Curtis'

__author__ = 'Curtis'
import yahoo
import benchScrape as bench
import complementsScrape as comp
import random

from pymongo import Connection, DESCENDING, ASCENDING, MongoClient
global client
client = MongoClient()
global conn
conn = Connection().Bench
global comments
comments = conn.comments
global complements
complements = conn.complements


class BenchScene:
    def __init__(self, increase, get_more, debug, filter):
        self.getLines(get_more)
        self.printScript(increase, debug, filter)

    def getLines(self, more):
        found_comments = comments.find({})

        if found_comments.count() < 100 or more:
            bench.getMoreComments()
            print("Getting compliments\n")
            comp.getMoreComments()
        #print("Done")

    def printScript(self, increase, debug, filter):
        print("SCRIPT:")
        script = self.generateScript(increase, debug, filter)
        for line in script:
            print(line)

    def generateScript(self, increase, debug, filter):
        script = []
        # get comments corresponding to each "score"
        if increase == 'increase':
            # start with several of score 1, increase score
            #print("Escalating vulgarity.")
            first_comment = ""
            last_comment = ""
            first = 0
            '''
            for i in range(1,11):
                lines = comments.find({'vulgarity_score': i})
                count = lines.count()
                #print("There are " + str(count) + " entries of score " + str(i))
                if count > 0:

                    rand_line = random.randint(0, count-1)

                    line = lines[rand_line]

                    if first == 0:
                        first_comment = line['text']
                        first = 1

                    print("Actor " + str(i) + ": " + line['text'] + "\n" + "\t\tMax feature:\t" + line['max_feature'] +
                            " score " + str(line['feature_score']))

            '''
            max_swears = 1
            if filter == True:
                max_swears = 0
                script.append("Filtered.")
            num = 0
            for i in range(1, 8):
                lines = comments.find({'feature_score': i})
                count = lines.count()
                if debug == True:
                    script.append("There are " + str(count) + " entries of score " + str(i))
                if count > 0:
                    num += 1
                    rand_line = random.randint(0, count-1)
                    line = lines[rand_line]


                    if i < 5:
                        n = 1
                        while line['swears'] > max_swears:
                            if n > 400:
                                break
                            n += 1
                            rand_line = random.randint(0, count-1)
                            line = lines[rand_line]

                    if i > 5 and filter == True:
                        continue

                    if first == 0:
                        first_comment = line['text']
                        first = 1
                    script.append("Actor " + str(num) + ": " + line['text'])
                    if debug == True:
                        script.append("\t\tMax feature:\t" + line['max_feature'] + " score " + str(line['feature_score']))

            all_complements = complements.find({})
            complements_count = all_complements.count()
            rand_complement = random.randint(0, complements_count-1)
            #last_comment = all_complements[rand_complement]['text'] + "\n" + first_comment

            last_line = "Last Actor: " + all_complements[rand_complement]['text']
            last_comment = "First Actor: " + first_comment
            script.append(last_line)
            script.append(last_comment)
        return script


if __name__ == '__main__':
    # BenchScene(increase, get_more, debug, filter)
    # if filtered, will not print any with swears, stops after 5 actors
	scene = BenchScene('increase', False, True, False) # true will take longer due to large amounts of comments


