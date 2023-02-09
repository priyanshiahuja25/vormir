import praw
import os
from dotenv import load_dotenv

# My Classes
from src.video_content import VideoContent
from src.comment import Comment

load_dotenv()


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
    video_content.make_audio()
    video_content.make_video()


if __name__ == "__main__":
    main()
