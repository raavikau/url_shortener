import json
import random
import string
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

shortened_urls = {}
def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form['long_url']
        short_url = generate_short_url()
        while short_url in shortened_urls:  # Ensuring Uniqueness of the Short URL
            short_url = generate_short_url()
        shortened_urls[short_url] = long_url
        with open("urls.json", "w") as data:
            json.dump(shortened_urls, data)
        return f"shortened url: {request.url_root}{short_url}"
    return render_template("index.html")

@app.route("/<short_url>")
def redirect_url(short_url):
    long_url =shortened_urls.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "Url not found", 404
if __name__ == '__main__':
    with open("urls.json", "r") as data:
        shortened_urls = json.load(data)
    app.run(debug=True)
