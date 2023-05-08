from src.comment import Comment
import os


class VideoContent:
    def __init__(self, title, url, username, submission_id, score):
        self.url = url
        self.submission_id = submission_id
        self.username = username
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
