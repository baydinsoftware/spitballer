import datetime
from demo.models import Post, Comment
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.template.loader  import render_to_string
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def main(request):
	# Ensures that post-dated posts will not be posted and prevents a large query of all available Posts
	latest_post_list = Post.objects.filter(date__lte =datetime.datetime.now()).order_by('date').reverse()
	context = {'latest_post_list' : latest_post_list}
	return render(request, 'demo/main.html', context)

@login_required
def index(request, user):
	
	# Access granted to user only if username in URL matches the request.user logged in at the moment
	if user==request.user.username and request.user.is_authenticated():
		latest_post_list = Post.objects.filter(date__lte=datetime.datetime.now()).order_by('date').reverse()[:10]
		comment_list = Comment.objects.filter(date__lte=datetime.datetime.now()).order_by('post')
		
		context = {'latest_post_list':latest_post_list, 'comment_list':comment_list }
		return render(request, 'demo/index.html', context)
	
	# If a spoofed username is attempted in URL, redirects to currently logged in users home page
	return HttpResponseRedirect('/' + request.user.username)

@login_required
def add_post(request, user):
	results = {'success' : False}
	
	if request.method == u'GET':
	  	# USe POST	
		GET = request.GET
		if GET.has_key(u'text'):
			
			post = Post (text = GET[u'text'], user = request.user, date = datetime.datetime.now())
			post.save()
			
			html = render_to_string('demo/post.html', {'post' : post})
			results = {'success':True, 'html' : html}
	
	json = simplejson.dumps(results)
	return HttpResponse (json, mimetype='application/json')

@login_required
def add_comment(request, user, post_id):
	results = {'success' : False}
	
	if request.method == u'GET':
		
		GET = request.GET
		if GET.has_key(u'text'):
			
			comment = Comment (text = GET[u'text'], user = request.user, date = datetime.datetime.now(), post = Post.objects.get(id=GET[u'postid']))
			comment.save()
			
			html = render_to_string('demo/comment.html', {'comment' : comment})
			results = {'success':True, 'html':html, 'id':comment.post.id}
	
	json = simplejson.dumps(results)
	return HttpResponse (json, mimetype='application/json')

@login_required
def detail(request, post_id):
	comment_list = Comment.objects.order_by('date')
	post = get_object_or_404(Post, pk=post_id)
	return render(request, 'demo/detail.html', {'post' : post, 'comment_list' : comment_list})

@login_required
def user(request, user):
	profile = User.objects.get(username=user)
	return HttpResponse("You're looking at the user %s." % profile.username)

def login_user(request):
        state = "Please log in below..."
        username = password = ''
        
	if request.POST:
                username = request.POST.get('username')
                password = request.POST.get('password')

                user = authenticate(username=username, password=password)
                if user is not None:
                        if user.is_active:
                                login (request, user)
                                info = {'user' : user}
                                url = '/' + user.username
                                return HttpResponseRedirect(url)
                        else:
                                state = "Your account is not active, please contact the site admin."
                                return render(request, 'demo/auth.html', {'state' : state})
                else:
                        state = "Your username and/or password were incorrect."
                        return render(request, 'demo/auth.html', {'state' : state})
        else:
                info = {'state' : state}
                return render(request, 'demo/auth.html', info)

@login_required
def logout_user(request, user):
        logout(request)
        return redirect('/')

