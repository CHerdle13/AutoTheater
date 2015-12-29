__author__ = 'Misha Kushnir'

import bachelorSceneNew, benchScene
from flask import Flask, render_template, request, url_for, redirect
app = Flask(__name__)

@app.route("/")
def homepage():
    try:
        title = "Auto Theater"
        paragraph = ["Auto Theater is an AI project that scrapes the internet to generate custom improv scripts.",
                     "Pick one of the improv games above to get started."]
        return render_template("main.html", title=title, paragraph=paragraph)
    except Exception as e:
        return "Error:\n" + str(e)

@app.route("/about/")
def aboutpage():
    try:
        title = "About Auto Theater"
        paragraph = ["Built for Prof. Larry Birnbaum's EECS 338 class in Fall 2015 by Michael Kushnir, Curtis Wiese, Marc Malinowski and Craig Herdle.",
                     "Contact: michaelkushnir2015@u.northwestern.edu"]
        pageType = "about"
        return render_template("main.html", title=title, paragraph=paragraph, pageType=pageType)
    except Exception as e:
        return "Error:\n" + str(e)

@app.route("/bachelor/", methods=['GET','POST'])
def bachelor():
    try:
        title = "The Bachelor"
        paragraph = ["A game about questions.","One actor asks the others questions and sees what they have to say."]
        game = "Bachelor"
        if request.method == "POST":
            actors = int(request.form["actors"])
            topic = request.form["topic"]
            skipDownload = None
            # there definitely has to be a better way to get the checkbox value
            try:
                request.form["skipDownload"]
                skipDownload = True
            except:
                skipDownload = False
            questions = int(request.form["questions"])
            if actors <= 0:
                return "You must have more than 0 actors."
            else:
                scene = bachelorSceneNew.BachelorScene(actors, [topic], "Reddit", questions, skipDownload)
                script = scene.generateScript()
                return render_template("main.html", title=title, paragraph=paragraph, game=game, script=script)
        else:
            return render_template("main.html", title=title, paragraph=paragraph, game=game)
    except Exception as e:
        print("Error:\n" + str(e))
        return "Error:\n" + str(e)

@app.route("/scared_off_the_bench/", methods=['GET','POST'])
def scaredOffTheBench():
    try:
        title = "Scared Off the Bench"
        paragraph = ["A game about shock.","One actor sits on the bench, and the others try to force him to give up his spot."]
        game = "Scared Off the Bench"
        if request.method == "POST":
            #actors = int(request.form["actors"])
            #topic = request.form["topic"]
            debug = None
            # there definitely has to be a better way to get the checkbox value
            try:
                request.form["debug"]
                debug = True
            except:
                debug = False
            profanityFilter = None
            try:
                request.form["profanity"]
                profanityFilter = True
            except:
                profanityFilter = False
            increase = "increase"
            scene = benchScene.BenchScene(increase, False, debug, profanityFilter)
            script = scene.generateScript(increase, debug, profanityFilter)
            return render_template("main.html", title=title, paragraph=paragraph, game=game, script=script)
        else:
            return render_template("main.html", title=title, paragraph=paragraph, game=game)
    except Exception as e:
        return "Error:\n" + str(e)

if __name__ == "__main__":
    app.run()