import json
import random
import string
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

short_url_dict = {}  # dictionary to store mapping of short to long URL
def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form['long_url']  # get long url from form submission
        short_url = generate_short_url()  # generate short url
        while short_url in short_url_dict:  # ensure uniqueness of the short url
            short_url = generate_short_url()
        short_url_dict[short_url] = long_url  # store short url and long url in dictionary
        with open("urls.json", "w") as data:
            json.dump(short_url_dict, data)
        return render_template("index.html", short_url=short_url)
    return render_template("index.html")

@app.route("/<short_url>")
def redirect_url(short_url):
    # long_url =short_url_dict.get(short_url)
    if short_url in short_url_dict:  # check if short url in dictionary
        long_url = short_url_dict[short_url]  # ge long url corresponding to short url
        return redirect(long_url)  # redirect to long url
    else:
        return "Url not found", 404  # if url not exists
if __name__ == '__main__':
    with open("urls.json", "r") as data:
        short_url_dict = json.load(data)
    app.run(debug=True)
