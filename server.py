# Imports
from flask import Flask, request, render_template, abort
import praw
import os
from dotenv import load_dotenv

# My Classes
from src.video_content import VideoContent
from src.comment import Comment

# Flask instance
app = Flask(__name__)

load_dotenv()

# Instantiating a reddit instance using .env file details
reddit = praw.Reddit(
    client_id=os.environ['CLIENT'],
    client_secret=os.environ['SECRET'],
    user_agent=os.environ['USER_AGENT']
)


@app.route('/')
def hello_world():
    """Homepage Route; as of now its only purpose is url taking"""
    return render_template('index.html')


@app.route('/make')
def make():
    """MakeVideo Route; video starts being made"""
    try:
        video_content = get_reddit_data(request.args.get('url'))
        if video_content is None:
            raise Exception("Error in getting post data")
        video_content.make_images()
        return render_template('make.html', video_content=video_content)
    except Exception as e:
        abort(404, e)


def get_reddit_data(url):
    """Function to get the reddit data"""
    submission_r = reddit.submission(url=url)
    submission_r.comment_sort = 'top'
    video_content = VideoContent(title=submission_r.title, username=submission_r.author, url=submission_r.url, submission_id=submission_r.id,
                                 score=submission_r.score)
    submission_r.comments.replace_more(limit=0)

    for comment_r in submission_r.comments[:5]:
        new_comment = Comment(body=comment_r.body, username=comment_r.author, comment_id=comment_r.id, score=comment_r.score)
        if not video_content.add_comment(new_comment):
            return None

    return video_content


@app.errorhandler(404)
def page_not_found(error):
    """HTTP 404 error handler any request that gives 404 will be redirected here"""
    return render_template('error.html', error_code=404, error=error.description), 404
