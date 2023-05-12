from src.comment import Comment
import os
import praw
from selenium import webdriver
from selenium.webdriver import Keys
import time

# Instantiating a reddit instance using .env file details
reddit = praw.Reddit(
    client_id=os.environ['CLIENT'],
    client_secret=os.environ['SECRET'],
    user_agent=os.environ['USER_AGENT']
)

class VideoContent:
    def __init__(self, url, submission_id):
        self.url = url
        self.submission_id = submission_id
        self.comments = []
        self.path = VideoContent.make_folder(submission_id)

    def make_images(self):
        try:
            driver = webdriver.Chrome()
        except:
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
            post_title = driver.find_element('css selector', '.Post')
            post_title.screenshot(os.path.join(self.path, 'title.png'))

            driver.get(self.url + "?sort=top")
            comments = driver.find_elements('css selector', ".Comment")[:5]
            for comment in comments:
                comment_id = comment.get_attribute("class").split()[1][3:]
                comment.screenshot(os.path.join(self.path, f'{comment_id}.png'))
                comment_content = reddit.comment(comment_id)
                new_comment = Comment(comment_id=comment_id, path=os.path.join(self.path, f'{comment_id}.png'),
                                      body=comment_content.body)

                self.comments.append(new_comment)

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
