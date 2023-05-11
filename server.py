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
# reddit = praw.Reddit(
#     client_id=os.environ['CLIENT'],
#     client_secret=os.environ['SECRET'],
#     user_agent=os.environ['USER_AGENT']
# )


@app.route('/')
def hello_world():
    """Homepage Route; as of now its only purpose is url taking"""
    return render_template('index.html')


@app.route('/make')
def make():
    """MakeVideo Route; video starts being made"""
    try:
        id_index = request.args.get('url').find('/comments/')
        submission_id = request.args.get('url')[id_index+10:id_index+17]
        video_content = VideoContent(submission_id=submission_id, url=request.args.get('url'))

        video_content.make_images()
        return render_template('make.html', video_content=video_content)
    except Exception as e:
        abort(404, e)


@app.errorhandler(404)
def page_not_found(error):
    """HTTP 404 error handler any request that gives 404 will be redirected here"""
    return render_template('error.html', error_code=404, error=error.description), 404
