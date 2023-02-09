from .comment import Comment
from bs4 import BeautifulSoup
from html2image import Html2Image
import os
from gtts import gTTS, gTTSError
from moviepy.editor import *


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
        path = os.path.join(os.getcwd(), self.path, 'images')
        os.mkdir(path)

        hti = Html2Image(output_path=path, custom_flags=['--virtual-time-budget=1000', '--hide-scrollbars'])
        hti.size = (500, 350)
        try:
            template_file = os.path.join(os.getcwd(), 'assets', 'reddit_comment.html')
            for comment in self.comments:
                VideoContent.change_html(file_name=template_file, text=comment.body)
                hti.screenshot(html_file='assets/reddit_comment.html', css_file='assets/reddit_comment.css',
                               save_as=f'{comment.comment_id}.png')

            # TITLE SCREENSHOT
            hti.size = (550, 400)
            template_file = os.path.join(os.getcwd(), 'assets', 'reddit_title.html')
            VideoContent.change_html(file_name=template_file, text=self.title)
            hti.screenshot(html_file='assets/reddit_title.html', css_file='assets/reddit_title.css',
                           save_as='title.png')
        except Exception as e:
            print(e)
            print("Some Error Occurred")

    def make_audio(self):
        path = os.path.join(os.getcwd(), self.path, 'audio')
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

    def make_video(self):
        # Make Image Clips
        clips = []
        for comment in self.comments:
            comment_audio = AudioFileClip(filename=os.path.join(self.path, 'audio', f'{comment.comment_id}.mp3'),
                                          fps=44100)
            clips.append(ImageClip(os.path.join(self.path, 'images', f'{comment.comment_id}.png'))
                         .set_duration(t=comment_audio.duration + 1).set_audio(comment_audio))

        # Make title clip
        comment_audio = AudioFileClip(filename=os.path.join(self.path, 'audio', f'title.mp3'),
                                      fps=44100)
        clips.insert(0,
                     ImageClip(os.path.join(self.path, 'images', f'title.png')).set_duration(
                         t=comment_audio.duration + 1)
                     .set_audio(comment_audio))

        # Make the actual Video
        # print(clips)
        concat_clip = concatenate_videoclips(clips, method="compose")
        concat_clip.write_videofile(os.path.join(self.path, "main.mp4"), fps=24)

    @staticmethod
    def change_html(file_name, text):
        """I will make this method more reliable in the future maybe"""
        # Load the HTML file
        with open(file_name) as f:
            soup = BeautifulSoup(f, "html.parser")

        # Find the specific tag you want to change
        tag = soup.find("p", {"class": "content"})

        # Change the text of the tag
        tag.string = text

        # Save the modified HTML file
        with open(file_name, "w") as f:
            f.write(str(soup))

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
