from datetime import datetime


class User:
    def __init__(self, user_id, username, email, bio):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.bio = bio
        self.following = set()
        self.followers = set()
        self.posts = []

    def follow(self, user):
        self.following.add(user.user_id)
        user.followers.add(self.user_id)

    def unfollow(self, user):
        self.following.remove(user.user_id)
        user.followers.remove(self.user_id)

    def is_following(self, user):
        return user.user_id in self.following

    def is_followed_by(self, user):
        return user.user_id in self.followers


class Post:
    def __init__(self, post_id, userId, caption):
        self.post_id = post_id
        self.userId = userId
        self.posted_image
        self.caption = caption
        self.date_posted = datetime.now()
        self.comments = []

    def add_comment(self, comment):
        self.comments.append(comment)

    def get_comments(self):
        return self.comments

    def get_posted_image(self):
        return self.posted_image
    
    
