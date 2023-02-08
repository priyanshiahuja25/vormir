from moviepy.editor import *
import praw
from dotenv import load_dotenv
import os

load_dotenv()


class VideoContent:
    def __init__(self, title, url, submission_id, score):
        self.url = url
        self.submission_id = submission_id
        self.title = title
        self.comments = []
        self.score = score

    def add_comment(self, comment):
        if isinstance(comment, Comment):
            self.comments.append(Comment)
            return True
        else:
            print("Invalid Object Type, Should Be Of Type Comment")
            return False

    def __str__(self):
        print(type(self.title))
        return f"{self.title} \n- Comments {len(self.comments)}"


class Comment:
    def __init__(self, comment_id, body, score):
        self.comment_id = comment_id,
        self.body = body,
        self.score = score

    def __str__(self):
        return self.body


def get_reddit_data(url):
    reddit = praw.Reddit(
        client_id=os.environ['CLIENT'],
        client_secret=os.environ['SECRET'],
        user_agent=os.environ['USER_AGENT']
    )

    submission_r = reddit.submission(url=url)
    submission_r.comment_sort = 'top'
    video_content = VideoContent(title=submission_r.title, url=submission_r.url, submission_id=submission_r.id,
                                 score=submission_r.score)
    submission_r.comments.replace_more(limit=0)

    for comment_r in submission_r.comments[:5]:
        new_comment = Comment(body=comment_r.body, comment_id=comment_r.id, score=comment_r.score)
        if not video_content.add_comment(new_comment):
            print(f"Comment {comment_r.title}")
            return None

    return video_content


def make_video(video_content):
    pass


def main():
    url_to_post = input("URL To Post: ")
    video_content = get_reddit_data(url_to_post)

    if not video_content:
        print("Error In Getting Data")
        exit()

    make_video(video_content)


if __name__ == "__main__":
    main()
