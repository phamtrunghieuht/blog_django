from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Comment
from django.views.generic import DetailView, ListView
from marketing.models import Signup
from django.http import HttpResponseRedirect
# Create your views here.

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains = query) |
            Q(description__icontains = query)
        )
    context = {
        'queryset': queryset
    }

    return render(request, 'search_result.html', context)

def get_category_count():
    queryset = Category.objects.values('title').annotate(Count('post'))
    return queryset

def index(request):
    featured = Post.objects.filter(featured = True)
    latest = Post.objects.order_by('-created')[0:3]
    
    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'featured_post': featured,
        'most_recent': latest
    }
    return render(request, 'index.html',context)

def blog(request):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-created')[:3]
    article_post = Post.objects.all()
    paginator = Paginator(article_post, 2)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'category_count': category_count,
        'most_recent': most_recent,
        'article_post': paginated_queryset,
        'page_request_var': page_request_var
    }
    return render(request, 'blog.html',context)

def post(request, post):
    #sidebar
    category_count = get_category_count()
    print(category_count)
    most_recent = Post.objects.order_by('-created')[:3]
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    #post
    obj_post = get_object_or_404(Post, slug=post)
    obj_post.views += 1
    obj_post.save()

    #comment post
    if request.method == "POST":
        username = request.POST["username"]
        content = request.POST["usercomment"]
        new_comment = Comment()
        new_comment.username = username
        new_comment.content = content
        new_comment.post = obj_post
        new_comment.save()
        return HttpResponseRedirect(request.path)
        
    context = {
        'blog_post':obj_post,
        'category_count': category_count,
        'most_recent': most_recent
    }
    return render(request, 'post.html',context)

def categoryView(request,title):
    posts = Post.objects.filter(categories__title=title)
    print(posts)
    context = {
        'queryset': posts
    }
    return render(request,'category.html',context)