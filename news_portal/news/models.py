from django.db import models


class Author(models.Model):

    def update_rating(self):
        pass


class Category(models.Model):
    pass


class Post(models.Model):

    def like(self):
        pass

    def dislike(self):
        pass


class PostCategory(models.Model):
    pass


class Comment(models.Model):

    def like(self):
        pass

    def dislike(self):
        pass
