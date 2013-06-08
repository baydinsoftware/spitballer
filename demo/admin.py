import datetime
from demo.models import Post, Comment
from django.http import HttpResponseRedirect
from django.contrib import admin
from django.contrib.auth.models import User


class CommentInline(admin.StackedInline):
	model = Comment
	extra = 1

class PostAdmin(admin.ModelAdmin):
	# Delares what info will show in list view of ALL posts	
	list_display = ('text', 'user')
	# Declares Fieldsets for Indv. Post View
	fieldsets = [
		(None, {'fields': ['user']}),
		('Message Info', {'fields': ['date', 'text']})
	]
	# Describes the inline comments that can be added to each post
	inlines = [CommentInline]

	def response_add(self, request, obj, post_url_continue=None):
		if request.POST.has_key("_postlater") and obj.date > datetime.datetime.now():
                        msg = "The post: %s will be posted on %s" % (obj.text, obj.date.strftime("%a %d %B, %Y at %I:%M %p %Z"))
                        self.message_user(request, msg)
                        return HttpResponseRedirect("../")
                elif request.POST.has_key("_postlater") and obj.date <= datetime.datetime.now():
                        msg = "Date set before current time. Did you want to post now? If so, Click Post Now. Otherwise, modify date so that it comes later than the current one."
                        self.message_user(request, msg)
                        return HttpResponseRedirect("")
		else:
			return super(PostAdmin, self).response_add(request, obj)
	
	def response_change(self, request, obj, *args, **kwargs):
		if request.POST.has_key("_postlater") and obj.date > datetime.datetime.now():
			msg = "The post: %s will be posted on %s" % (obj.text, obj.date.strftime("%a %d %B, %Y at %I:%M %p %Z"))
			self.message_user(request, msg)
			return HttpResponseRedirect("../")		
		elif request.POST.has_key("_postlater") and obj.date <= datetime.datetime.now():
			msg = "Date set before current time. Did you want to post now? If so, Click Post Now. Otherwise, modify date so that it comes later than the current one."
			self.message_user(request, msg)
			return HttpResponseRedirect("")
		elif request.POST.has_key('_saveback'):
			obj.save()
			return HttpResponseRedirect("../")
		else:
			obj.date = datetime.datetime.now()
			return super(PostAdmin, self).response_change(request, obj)
		 	
admin.site.register(Post, PostAdmin)
