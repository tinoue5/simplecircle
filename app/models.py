from django.db import models
from django.contrib.auth.models import User

# Circle - サークル
class Circle(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=64)

# Joining - ユーザがサークルに入っている紐付け
class Joining(models.Model):
    def __str__(self):
        return self.circle.name + " hires " + str(self.user)
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# CircleInvitation - サークルへの招待
class CircleInvitation(models.Model):
    def __str__(self):
        return 'invitation of ' + str(self.circle)
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE)
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.TextField('Random Hash')
    expired_at = models.DateTimeField('Expired At')

# Message - サークルの伝言板
class Message(models.Model):
    def __str__(self):
        return 'message at' + str(self.posted_at)
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE)
    user_posted = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField('Message Body')
    posted_at = models.DateTimeField('Posted At')
