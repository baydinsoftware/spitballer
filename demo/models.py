import datetime
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
	text = models.CharField(max_length=160)
	date = models.DateTimeField('Publish Date', default=datetime.datetime.now())
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.text
	
	def get_absolute_url(self):
		return "post/%d" % self.id

class Comment(models.Model):
	text = models.CharField(max_length=160)
	date = models.DateTimeField('Publish Date', default=datetime.datetime.now())
	user = models.ForeignKey(User)
	post = models.ForeignKey('Post')

	def __unicode__(self):
		return self.text
