from flask import Flask, render_template, jsonify, redirect
import pymongo
import nasa_scrape

app = Flask(__name__)

conn = 'mongodb://localhost:27017'

client = pymongo.MongoClient(conn)

db = client.NASA

@app.route("/")
def index():
    NASA = list(db.images.find())
    return render_template("index.html", NASA=NASA)

@app.route("/scrape")
def scrape():
    NASA = list(db.images.find())
    nasa_data = nasa_scrape.scrape()
    NASA.update(
        {},
        nasa_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)