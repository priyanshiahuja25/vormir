class Comment:
    def __init__(self, comment_id, body, score):
        self.comment_id = comment_id
        self.body = body
        self.score = score

    def __str__(self):
        return self.body
