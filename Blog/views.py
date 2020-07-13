from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Post, Categories,Comment
from.forms import ContactForm, CommentForm

import hitcount
from hitcount.models import HitCount
from hitcount.views import HitCountMixin


def home(request):
    categories = Categories.objects.all()

    recent_news = Post.objects.filter(status=1).order_by('-created_on')
    trending = Post.objects.filter(status=1, trending=True).order_by('-created_on')[:5]
    popular = Post.objects.order_by('hit_count_generic')[:5]

    politics_posts = Post.objects.filter(status=1, category__name='Politics').order_by('-created_on')[:5]
    sports_posts = Post.objects.filter(status=1, category__name='Sports').order_by('-created_on')[:5]
    editors_picks = Post.objects.filter(status=1, editors_pick=True)
    editors_pick_carousel = Post.objects.filter(status=1, editors_pick=True)[:3]

    head_post = [post for post in popular if post in editors_picks][:1]
    editors_pick = [post for post in editors_picks if post not in editors_pick_carousel][:4]

    paginator = Paginator(recent_news, 5)
    is_paginated = True if paginator.num_pages > 1 else False
    page_number = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj, 'politics_posts': politics_posts, 'sports_posts': sports_posts,
        'editors_pick': editors_pick, 'editors_pick_carousel': editors_pick_carousel, 'trending': trending,
        'categories': categories, 'popular': popular, 'is_paginated': is_paginated, 'head_post': head_post
        }
    return render(request, 'index.html', context)


def searchposts(request):
    categories = Categories.objects.all()
    popular = Post.objects.order_by('hit_count_generic')[:5]
    if request.method == 'GET':
        query = request.GET.get('q')
        categories = Categories.objects.all()

        if query is not None:
            lookups = Q(title__icontains=query) | Q(content__icontains=query)

            results = Post.objects.filter(lookups).distinct()

            paginator = Paginator(results, 5)
            is_paginated = True if paginator.num_pages > 1 else False
            page_number = request.GET.get('page') or 1
            page_obj = paginator.get_page(page_number)

            context = {'popular': popular, 'categories': categories, 'page_obj': page_obj, 'is_paginated': is_paginated}

            return render(request, 'searches.html', context)

        else:
            return render(request, 'searches.html', {'categories': categories, 'popular': popular})

    return render(request, 'searches.html', {'categories': categories, 'popular': popular})


def category(request, name):
    categories = Categories.objects.all()
    posts = Post.objects.filter(status=1, category__name=name).order_by('-created_on')
    popular = Post.objects.order_by('hit_count_generic')[:5]

    paginator = Paginator(posts, 5)
    is_paginated = True if paginator.num_pages > 1 else False
    page_number = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_number)

    context = {'categories': categories, 'popular': popular, 'name': name,
               'page_obj': page_obj, 'is_paginated': is_paginated
               }
    return render(request, 'categories.html', context)



def trending(request):
    trendings = Post.objects.filter(status=1, trending=True).order_by('-created_on')
    popular = Post.objects.order_by('hit_count_generic')[:5]
    categories = Categories.objects.all()
    name = 'Trending'

    paginator = Paginator(trendings, 5)
    is_paginated = True if paginator.num_pages > 1 else False
    page_number = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_number)

    context = {
        'popular': popular, 'categories': categories,
        'page_obj': page_obj, 'is_paginated': is_paginated, 'name': name
        }
    return render(request, 'categories.html', context)


def popular(request):
    all_popular = Post.objects.order_by('hit_count_generic')
    popular = Post.objects.order_by('hit_count_generic')[:5]
    categories = Categories.objects.all()
    name = 'Popular'

    paginator = Paginator(all_popular, 5)
    is_paginated = True if paginator.num_pages > 1 else False
    page_number = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': categories, 'popular': popular,
        'page_obj': page_obj, 'is_paginated': is_paginated, 'name': name
        }
    return render(request, 'categories.html', context)


def contact(request):
    categories = Categories.objects.all()
    if request.method =='GET':
        form = ContactForm
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            from_email = form.cleaned_data['email']
            tel_number = form.cleaned_data['tel_number']
            message = form.cleaned_data['message']
            try:
                subject = [first_name + ' ' + last_name + ',  ' + 'phone number: '  + str(tel_number)]
                send_mail(subject, message, from_email, ['youngbossravasco@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            send_mail(subject, message, from_email, ['youngbossravasco@gmail.com'])
            return HttpResponse('Thank you for your message.')

    context = {'form': form, 'categories': categories}
    return render(request, 'contact.html', context)


def blog_single(request, name, slug):
    Categories.objects.get(name=name)
    post = get_object_or_404(Post, slug=slug)
    categories = Categories.objects.all()
    popular = Post.objects.order_by('hit_count_generic')[:5]

    count_hit = True
    hit_count = HitCount.objects.get_for_object(post)
    hit_count_response = hitcount.views.HitCountMixin.hit_count(request, hit_count)
    # count the views
    event_views = post.hit_count.hits

    comments = post.comments.filter(active=True).order_by('-created_on')
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            print(new_comment)
            parent_obj = None
            try:

                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists and parent_qs.count() == 1:
                    parent_obj = parent_qs.first()
                    new_comment.parent = parent_obj
                    new_comment.save()
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {
        'categories': categories, 'post': post, 'comments': comments,
        'new_comment': new_comment, 'popular': popular, 'form': comment_form
    }
    return render(request, 'blog-single.html', context)

