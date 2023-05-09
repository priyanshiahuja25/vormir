from src.comment import Comment
import os

from selenium import webdriver
from selenium.webdriver import Keys
import time


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

    def make_images(self):
        driver = webdriver.Firefox()
        try:
            driver.get("https://www.reddit.com/login")
            username_field = driver.find_element("css selector", "#loginUsername")
            password_field = driver.find_element("css selector", "#loginPassword")

            # enter your login credentials
            username_field.send_keys("Broken-Back-16")
            password_field.send_keys("@Uday1601")

            # submit the login form
            password_field.send_keys(Keys.RETURN)

            time.sleep(5)
        except Exception as e:
            print(e)
            # quit the driver only if there is an error
            driver.quit()
        else:
            driver.get(self.url)
            post_title = driver.find_element(value="t3_"+self.submission_id)
            post_title.screenshot(os.path.join(self.path, 'title.png'))

            driver.get(self.url+"?sort=top")
            for comment in self.comments:
                try:
                    ele = driver.find_element('css selector', ".Comment.t1_"+comment.comment_id)
                    ele.screenshot(os.path.join(self.path, self.comments[0].comment_id+".png"))
                except Exception as e:
                    print(e)
        finally:
            driver.quit()

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



