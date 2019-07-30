from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic. base import TemplateView
from .forms import BlogForm, CommentForm, HashtagForm
from .models import Blog, Comment, Hashtag
# Create your views here.
def layout(request):
    return render(request, 'blog/layout.html')

def home(request):
    blogs = Blog.objects
    hashtags = Hashtag.objects
    return render(request, 'blog/home.html', {'blogs': blogs, 'hashtags':hashtags})

class MainpageView(TemplateView):
    template_name = 'blog/main.html'
    
def detail(request, blog_id, comment=None): #근데 여기에 굳이 None을 왜해준거지?
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog_id = blog
            comment.comment_text = form.cleaned_data["comment_text"]
            comment.save()
            return redirect("blog:detail", blog_id)        
    else:
        form = CommentForm(instance=comment)
        return render(request, "blog/detail.html",{"blog":blog, "form":form})

def blogform(request, blog_id=None):
    if request.method =='POST':
        form = BlogForm(request.POST, request.FILES, instance=blog_id)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.pub_date=timezone.now()
            blog.save()
            form.save_m2m()
            return redirect('blog:home')
    else:
        form = BlogForm(instance=blog_id)
        return render(request, 'blog/new.html', {'form':form})

def edit(request,blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return blogform(request, blog) #blogform 함수를 호출 리턴

def remove(request, blog_id):
    blog =get_object_or_404(Blog, id=blog_id)
    blog.delete()
    return redirect('blog:home')

def edit_comment(request, blog_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    return detail(request, blog_id, comment)

def remove_comment(request, blog_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('blog:detail', blog_id)
    
def hashtagform(request, hashtag=None):
    if request.method == 'POST':
        form = HashtagForm(request.POST, instance=hashtag)
        if form.is_valid():
            hashtag=form.save(commit=False)
            if Hashtag.objects.filter(name=form.cleaned_data['name']):
                form = HashtagForm()
                error_message = "이미 존재하는 해시태그"
                return render(request, 'blog/hashtag.html',{'form':form, "error_message":error_message})
            else:
                hashtag.name=form.cleaned_data['name']
                hashtag.save()
                return redirect('blog:home')
    else:
        form = HashtagForm(instance=hashtag)
        return render(request, 'blog/hashtag.html', {'form':form})

def search(request, hashtag_id):
    hashtag = get_object_or_404(Hashtag, pk=hashtag_id)
    return render(request, 'blog/search.html', {'hashtag':hashtag})