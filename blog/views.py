from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView
import csv
from .forms import EmailPostForm
from django.core.mail import send_mail

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# def post_list(request):
#     object_list = Post.objects.all()
#     paginator = Paginator(object_list, 3) # 3 posts in each page
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#     # If page is not an integer deliver the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#     # If page is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)
#     return render(request, 'blog/post/list.html', {'page':page, 'posts': posts})
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})

def export_blog(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="file.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['Title', 'Slug', 'Author', 'Body', 'Publish'])
    for post in Post.objects.all().values_list('title', 'slug', 'author','body','publish'):
        writer.writerow(post)

    return response

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
            post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" 
            f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com',
            [cd['to']])
            sent = True
        
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'form': form, 'post': post, 'sent': sent})