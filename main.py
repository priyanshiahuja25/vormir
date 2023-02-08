# from moviepy.editor import *
import praw
import os
from dotenv import load_dotenv
from html2image import Html2Image

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
            self.comments.append(comment)
            return True
        else:
            print("Invalid Object Type, Should Be Of Type Comment")
            return False

    def make_images(self):
        path = os.path.join(os.getcwd(), VideoContent.make_folder(self.submission_id), 'images')
        os.mkdir(path)
        print(path)
        hti = Html2Image(output_path=path, custom_flags=['--virtual-time-budget=1000', '--hide-scrollbars'])
        hti.size = (500, 350)
        
        for comment in self.comments:
            try:
                hti.screenshot(html_file='assets/reddit_comment.html', css_file='assets/reddit_comment.css', save_as=f'{comment.comment_id}.png')
            except Exception as e:
                print(e)
                print("Some Error Occurred")

        hti.size = (550, 400)
        hti.screenshot(html_file='assets/reddit_title.html', css_file='assets/reddit_title.css', save_as='title.png')

    @staticmethod
    def make_folder(submission_id):
        i = 0
        while True:
            try:
                if i == 0:
                    path = submission_id
                else:
                    path = f"{submission_id} ({i})"
                os.mkdir(path)
                break
            except FileExistsError:
                i += 1

        return path

    def __str__(self):
        return f"{self.title} \n- Comments {len(self.comments)}"


class Comment:
    def __init__(self, comment_id, body, score):
        self.comment_id = comment_id
        self.body = body
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


def main():
    url_to_post = input("URL To Post: ")
    video_content = get_reddit_data(url_to_post)

    if not video_content:
        print("Error In Getting Data")
        exit()

    video_content.make_images()


if __name__ == "__main__":
    main()
