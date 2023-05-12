class Comment:
    def __init__(self, comment_id, path, body):
        self.comment_id = comment_id
        self.body = body
        self.path = path

    def __str__(self):
        return f"{self.comment_id} - {self.body}"
