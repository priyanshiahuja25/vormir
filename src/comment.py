class Comment:
    def __init__(self, comment_id, username, body, score):
        self.comment_id = comment_id
        self.username = username
        self.body = body
        self.score = score

    def __str__(self):
        return f"{self.comment_id} - {self.body}"
