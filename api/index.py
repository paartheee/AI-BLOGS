from flask import Flask, render_template
from fetcher import fetch_blog_posts

app = Flask(__name__, template_folder="../templates")

@app.route("/")
def home():
    print("Fetching latest blog posts...")
    blog_posts = fetch_blog_posts()

    formatted_posts = []
    for post in blog_posts:
        formatted_posts.append({
            "title": post["title"],
            "link": post["link"],
            "published": post["published"].strftime("%a, %d %b %Y %H:%M:%S") if post["published"] else "Unknown",
            "source": post["source"],
            "summary": post["summary"]
        })

    return render_template("index.html", posts=formatted_posts)

# Vercel requires `app` exposed at bottom
app = app
