from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Comment, Follow
from django.utils import timezone
from .forms import BlogForm, CommentForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from django.db.models import Subquery

# Create your views here.
def feed(request):
  user = request.user

  #로그인 상태
  if user.is_authenticated:
    # myfollow_list = Follow.objects.filter(follower = user) 
    feeds = Blog.objects.filter(author__in = Subquery(Follow.objects.filter(follower = user).values('target')))

    # user_id__in=Subquery(users.values('id'))

    paginator = Paginator(feeds, 10)
    page = request.GET.get('page')
    feed_posts = paginator.get_page(page)
    return render(request, 'feed.html', {'feedPost': feed_posts})
  else:
    #로그인 안된 상태
    blogs = Blog.objects.all() 

    paginator = Paginator(blogs, 10)
    page = request.GET.get('page')
    all_posts = paginator.get_page(page)
    return render(request, 'feed.html', {'allPost':all_posts})


def new(request):
  if request.method == 'POST':
    form = BlogForm(request.POST, request.FILES)
    if form.is_valid():
      new_blog = form.save(commit=False)
      new_blog.upload_date = timezone.now()
      new_blog.author = request.user
      new_blog.save()
      return redirect('blog:detail', new_blog.id)
    return redirect('feed')
  else:
    form = BlogForm()
    return render(request, 'new.html', {'form': form})
    

def edit(request, id):
  post = get_object_or_404(Blog, pk = id)
  if request.method == 'GET': 
    blog_form = BlogForm(instance = post)
    return render(request, 'edit.html', {'edit_form':blog_form})
  else: 
    blog_form = BlogForm(request.POST, request.FILES, instance = post)
    if blog_form.is_valid():
      edit_blog = blog_form.save(commit=False)
      edit_blog.upload_date = timezone.now()
      edit_blog.save()
    return redirect('/blog/post/'+str(id))


def delete(request, id):
  delete_review = Blog.objects.get(id = id)
  delete_review.delete()
  return redirect('feed')


def detail(request, id):
  post = get_object_or_404(Blog, pk=id)
  comments = Comment.objects.filter(post_id=id, comment_id__isnull=True)

  re_comments = []
  for comment in comments:
    re_comments += list(Comment.objects.filter(comment_id=comment.id))

  form = CommentForm()
  return render(request, 'detail.html', {'post':post, 'comments':comments, 're_comments':re_comments, 'form': form} )


def create_comment(request, post_id):
  if request.method == 'POST':
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit=False)
      comment.post_id = Blog.objects.get(pk=post_id)
      comment.writer = request.user
      comment.save()
  return redirect('/blog/post/' + str(post_id))


def create_re_comment(request, post_id, comment_id):
  if request.method == 'POST':
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit=False)
      comment.post_id = Blog.objects.get(pk=post_id)
      comment.comment_id = Comment.objects.get(pk=comment_id)
      comment.writer = request.user
      comment.save()
  return redirect('/blog/post/' + str(post_id))



def post_likes(request):
  if request.is_ajax():
    blog_id = request.GET.get('blog_id')
    post = Blog.objects.get(id=blog_id)

    user = request.user
    if post.like.filter(id = user.id).exists():
      post.like.remove(user)
      message = "좋아요 취소"
    else:
      post.like.add(user)
      message = "좋아요"
  context = {
    'like_count' : post.like.count(),
    'message' : message,
  }
  return HttpResponse(json.dumps(context), content_type="application/json")


def follow(request):
  if request.is_ajax():
    target_id = request.GET.get('target_id')
    target = User.objects.get(id = target_id)

    target_fwlist = Follow.objects.filter(target = target)
    # print(target_fwlist)
    user = request.user
    if target_fwlist.exists() and Follow.objects.filter(target=target, follower=user).exists():
      Follow.objects.get(target=target, follower=user).delete()
      # target_fwlist.follower.remove(user)
      message = "구독 취소"
    else:
      Follow.objects.create(target=target, follower=user)
      # target_fwlist.follower.add(user)
      message = "구독 신청"
    context = {
    'message' : message,
  }
  return HttpResponse(json.dumps(context), content_type="application/json")


def personal(request, id):
  # target = User.objects.get(id = id)
  target = get_object_or_404(User, id = id)
  blog_list = Blog.objects.filter(author = target)

  paginator = Paginator(blog_list, 5)
  page = request.GET.get('page')
  posts = paginator.get_page(page)

  is_follow = Follow.objects.filter(target=target, follower= request.user)
  print(is_follow, '<<<<<<isfollow')
  onePost = Blog.objects.filter(author = target)[:1]
  return render(request, 'personal.html', {'posts':posts, 'is_follow': is_follow, 'onePost': onePost})


def search(request):
  keyword = request.GET.get('keyword')
  search_list = Blog.objects.filter(Q(body__icontains=keyword)|Q(title__icontains=keyword)).distinct()
  paginator = Paginator(search_list, 10)
  page = request.GET.get('page')
  posts = paginator.get_page(page)
  return render(request, 'search.html', {'search_list':search_list, 'posts': posts})