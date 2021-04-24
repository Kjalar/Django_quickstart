from django.db import models


class Tweet(models.Model):
    text = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    photo = models.URLField(max_length=800, blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.id}. [{self.author.username}] {self.text}'


class Follow(models.Model):
    follower = models.ForeignKey('auth.User', related_name='follows', on_delete=models.CASCADE)
    follows = models.ForeignKey('auth.User', related_name='followers', on_delete=models.CASCADE)
    followed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower} -> {self.follows}'
