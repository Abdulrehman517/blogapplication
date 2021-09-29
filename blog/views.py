import csv
import pandas
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls.base import reverse
from django.views.generic import ListView
from taggit.models import Tag

from .forms import CommentForm, EmailPostForm
from .models import Comment
from api.models import Post


def post_list(request, tag_slug=None):
    object_list = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 6) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page':page, 'posts': posts, 'tag':tag})


# class PostListView(ListView,):
#     queryset = Post.published.all()
   
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, publish__month=month, publish__day=day)
     # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
    # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
    # Assign the current post to the comment
            new_comment.post = post
    # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blog/post/detail.html', {'post': post, 'comment_form': comment_form, 'comments':comments, 'new_comment':new_comment, 'similar_posts':similar_posts})


def export_blog(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="file.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['Title', 'Slug', 'Author', 'Body', 'Publish', 'status'])
    for post in Post.objects.all().values_list('title', 'slug', 'author', 'body', 'publish', 'status'):
        writer.writerow(post)

    return response


def upload_csv(request):
    if request.method == "GET":
        return render(request, 'blog/post/upload_csv.html',)

    else:
        file = request.FILES['csv_file']
        if not file.name.endswith('.csv'):
            return HttpResponse('File is not CSV type')
        df = pandas.read_csv(file)
        for index, row in df.iterrows():
            data_dict = {'title': row['Title'], 'slug': row['Title'], 'Author': row['Author'], 'Body': row['Body'],
                         'Publish': row['Publish'], 'Status': row['Status']}

            Post.objects.create(title=data_dict["title"], slug=data_dict["slug"], body=data_dict["Body"],
                            author_id=data_dict["Author"], publish=data_dict['Publish'], status=data_dict['Status'])

        # return HttpResponse('Upload Successfull!')
        return render(request, 'blog/post/succes.html', )



        #
        # file_data = csv_file.read().decode("utf-8")
        # lines = file_data.split("\n")
        # for line in lines:
        #     fields = line.split(',')
        #     data_dict = {}
        #     data_dict["title"] = fields[0]
        #     data_dict["slug"] = fields[0]
        #     data_dict["author"] = fields[2]
        #     data_dict["body"] = fields[3]
        #     data_dict["publish"] = fields[4]
        #     data_dict["status"] = fields[5]
        # Post.objects.create(title=data_dict["title"], slug=data_dict["slug"], body=data_dict["body"],
        #                     author_id=data_dict["author"], publish=data_dict['publish'], status=data_dict['status'])
        # return HttpResponse('Upload Successfull!')


# data = {}
    # if request.method == "GET":
    #     return render(request, 'blog/post/upload_csv.html', data)
    #
    # else:
    #     csv_file = request.FILES['csv_file']
    #     if not csv_file.name.endswith('.csv'):
    #         return HttpResponse('File is not CSV type')
    #         # return redirect('/blog/upload_csv')
    # #if file is too large, return
    #     # if csv_file.multiple_chunks():
    #     #         return HttpResponse(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
    #     #         # return HttpResponseRedirect('blog/')
    #
    #     file_data = csv_file.read().decode("utf-8")
    #     lines = file_data.split("\n")
    #     for line in lines:
    #         fields = line.split(',')
    #         data_dict = {}
    #         data_dict["title"] = fields[0]
    #         data_dict["slug"] = fields[0]
    #         data_dict["author"] = fields[2]
    #         data_dict["body"] = fields[3]
    #         data_dict["publish"] = fields[4]
    #         data_dict["status"] = fields[5]
    #     Post.objects.create(title=data_dict["title"], slug=data_dict["slug"], body=data_dict["body"], author_id=data_dict["author"], publish=data_dict['publish'], status=data_dict['status'])
    #     return HttpResponse('Upload Successfull!')
    #

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
