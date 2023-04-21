class User:
    def __init__(self, user_id, username, email, password, bio):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
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
    def __init__(self, post_id, image_url, caption, author):
        self.post_id = post_id
        self.image_url = image_url
        self.caption = caption
        self.author = author
        self.likes = set()
        self.comments = []

    def add_like(self, user):
        self.likes.add(user.user_id)

    def remove_like(self, user):
        self.likes.remove(user.user_id)

    def add_comment(self, comment):
        self.comments.append(comment)

    def get_num_likes(self):
        return len(self.likes)

    def get_comments(self):
        return self.comments
