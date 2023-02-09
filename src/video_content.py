from .comment import Comment
from html2image import Html2Image
import os
from gtts import gTTS, gTTSError


class VideoContent:
    def __init__(self, title, url, submission_id, score):
        self.url = url
        self.submission_id = submission_id
        self.title = title
        self.comments = []
        self.score = score
        self.path = VideoContent.make_folder(submission_id)

    def add_comment(self, comment):
        if isinstance(comment, Comment):
            self.comments.append(comment)
            return True
        else:
            print("Invalid Object Type, Should Be Of Type Comment")
            return False

    def make_images(self):
        path = os.path.join(os.getcwd(), self.submission_id, 'images')
        os.mkdir(path)

        hti = Html2Image(output_path=path, custom_flags=['--virtual-time-budget=1000', '--hide-scrollbars'])
        hti.size = (500, 350)
        try:
            for comment in self.comments:
                hti.screenshot(html_file='assets/reddit_comment.html', css_file='assets/reddit_comment.css',
                               save_as=f'{comment.comment_id}.png')

            # TITLE SCREENSHOT
            hti.size = (550, 400)
            hti.screenshot(html_file='assets/reddit_title.html', css_file='assets/reddit_title.css',
                           save_as='title.png')
        except Exception as e:
            print(e)
            print("Some Error Occurred")

    def make_audio(self):
        path = os.path.join(os.getcwd(), self.submission_id, 'audio')
        os.mkdir(path)

        language = 'en'
        try:
            for comment in self.comments:
                audio = gTTS(text=comment.body, lang=language, tld='co.in', slow=False)
                audio.save(savefile=os.path.join(path, f'{comment.comment_id}.mp3'))

            # TITLE AUDIO
            audio = gTTS(text=self.title, lang=language, tld='co.in', slow=False)
            audio.save(savefile=os.path.join(path, f'title.mp3'))

        except gTTSError:
            print("Error In Making Audio")
            exit()

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

        return os.path.join(os.getcwd(), path)

    def __str__(self):
        return f"{self.title} \n- Comments {len(self.comments)}"
