from cs50 import SQL
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

db = SQL("sqlite:///final.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gallery", methods=["GET","POST"])
def gallery():
    if request.method == "GET":
        rows = db.execute("SELECT * FROM pictures")
        nums = {}
        temp= 1
        length = len(rows)
        for row in rows:
            nums[row["Name"]]=temp
            temp+=1
    else:
        tag = request.form.get("tag").lower()
        rows = db.execute('SELECT * FROM pictures WHERE name IN (SELECT Name FROM tags WHERE tag="' + tag + '")')
        nums = {}
        temp= 1
        length = len(rows)
        for row in rows:
            nums[row["Name"]]=temp
            temp+=1
        if length == 0:
            return redirect("/tagsError")
    return render_template("gallery.html", rows=rows, nums=nums, length=length)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/history")
def history():
    return render_template("history.html")

@app.route("/tags")
def tags():
    rows = db.execute("SELECT tag, count(*) AS Tagcount FROM tags GROUP BY tag")
    return render_template("tags.html",rows=rows)

@app.route("/tagsError")
def tagsError():
    rows = db.execute("SELECT tag, count(*) AS Tagcount FROM tags GROUP BY tag")
    return render_template("tags.html",rows=rows, noReturns=True)
