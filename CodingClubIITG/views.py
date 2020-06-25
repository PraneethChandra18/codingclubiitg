from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import *
from .forms import *
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from django.core.mail import send_mail
from mysite.settings import EMAIL_HOST_USER
# Create your views here.

from django.shortcuts import get_object_or_404
def index(request):
    if not request.user.is_authenticated:
        user=''
        return render(request, 'CodingClubIITG/index.html',{'user':user})
    else:
        user = request.user
        favorite_events = Favorite_events.objects.filter(for_user=user)
        favorite_projects = Favorite_projects.objects.filter(for_user=user)
        return render(request, 'CodingClubIITG/index.html',{'favorite_events':favorite_events,'favorite_projects':favorite_projects,'user':user})

def aboutus(request):
    members=Members.objects.all()

    return render(request,'CodingClubIITG/aboutus.html',{'members': members})


def events(request):
    events=Event.objects.all().order_by("-date")
    fav_events=[]
    if not request.user.is_authenticated:
        user=''
    else:
        user = request.user
        fav = Favorite_events.objects.filter(for_user=user)
        for f in fav:
            fav_events.append(f.event)

    return render(request, 'CodingClubIITG/events.html', {'events':events,'fav_events':fav_events,'user':user})

def event_detail(request, pk):
    event = Event.objects.get(pk=pk)
    comments = Discussion_events.objects.filter(event=event,replied_to__isnull=True)
    if not request.user.is_authenticated:
        user=''
    else:
        user = request.user

    return render(request, "CodingClubIITG/event_detail.html", {
        "event": event,
        'comments':comments,'event_id':pk,'user':user
    })

def blog(request):
    return render(request, 'CodingClubIITG/blogone.html')


def projects(request):
    projects=Projects.objects.all().order_by("-date")
    fav_projects=[]
    if not request.user.is_authenticated:
        user=''
    else:
        user = request.user
        fav = Favorite_projects.objects.filter(for_user=user)
        for f in fav:
            fav_projects.append(f.project)

    return render(request, 'CodingClubIITG/projects.html',{'projects':projects,'fav_projects':fav_projects,'user':user})

def project_detail(request, pk):
    project = Projects.objects.get(pk=pk)
    comments = Discussion_projects.objects.filter(project=project,replied_to__isnull=True)
    if not request.user.is_authenticated:
        user=''
    else:
        user = request.user

    return render(request, "CodingClubIITG/project_detail.html", {
        "project": project,
        'comments':comments,'project_id':pk,'user':user
    })

def event_template(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'CodingClubIITG/blog.html', {"post": post})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)

                    return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'CodingClubIITG/register.html', {'form': form})

@login_required
def addProjects(request):
    if request.method=='POST':
        form = ProjectsForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            return redirect('index')
        else:
            return redirect('addprojects')

    else:
        form=ProjectsForm()
    return render(request, 'CodingClubIITG/addproject.html', {'form': form})


@login_required
def addEvents(request):
    if request.method=='POST':
        form = EventsForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            return redirect('index')
        else:
            return redirect('addEvents')

    else:
        form=EventsForm()
    return render(request, 'CodingClubIITG/addevent.html', {'form': form})

# ------------------------------------------------------------------------

#Favorites

@login_required
def favorite_event(request):
    pk = request.GET.get('inputValue')
    user = request.user
    event = Event.objects.get(pk=pk)
    f = Favorite_events(for_user=user,event=event)
    f.save()
    data = {
    'pk': pk
        }
    return JsonResponse(data)

@login_required
def unfavorite_event(request):
    pk = request.GET.get('inputValue')
    user = request.user
    event = Event.objects.get(pk=pk)
    f = Favorite_events.objects.get(for_user=user,event=event)

    f.delete()
    data = {
    'pk': pk
        }

    return JsonResponse(data)
@login_required
def unfavorite_event_all(request):
    user = request.user
    favorites = Favorite_events.objects.filter(for_user=user)
    for f in favorites:
        f.delete()
    favorites = Favorite_events.objects.filter(for_user=user)
    return redirect('index')

@login_required
def favorite_project(request):
    pk = request.GET.get('inputValue')
    user = request.user
    project = Projects.objects.get(pk=pk)
    f = Favorite_projects(for_user=user,project=project)
    print("hi")
    f.save()
    data = {
    'pk': pk
        }

    return JsonResponse(data)

@login_required
def unfavorite_project(request):
    pk = request.GET.get('inputValue')
    user = request.user
    project = Projects.objects.get(pk=pk)
    f = Favorite_projects.objects.get(for_user=user,project=project)

    f.delete()
    data = {
    'pk': pk
        }

    return JsonResponse(data)

@login_required
def unfavorite_project_all(request):
    user = request.user
    favorites = Favorite_projects.objects.filter(for_user=user)
    for f in favorites:
        f.delete()
    favorites = Favorite_projects.objects.filter(for_user=user)
    return redirect('index')
# -----------------------------------------------------------------------------------------

# Discussion Forum

# Events
@login_required
def comment_event(request,pk):
    comment = request.GET.get('comment')

    event = Event.objects.get(pk=pk)
    d = Discussion_events(user=request.user,event=event,text=comment)
    d.save()
    return redirect('event_detail',pk)

@login_required
def delete_comment_event(request,pk):
    comment = Discussion_events.objects.get(pk=pk)
    event_id = comment.event.pk
    comment.delete()
    return redirect('event_detail',event_id)

@login_required
def delete_reply_event(request,pk):
    comment = Discussion_events.objects.get(pk=pk)
    comment_id = comment.replied_to.pk
    comment.delete()
    return redirect('discussion_event_replies',comment_id)

def edit_comment_event(request):
    pk = request.GET.get('pk')
    comment = Discussion_events.objects.get(pk=pk)
    text = request.GET.get('inputValue')
    event_id = comment.event.pk
    comment.text = text
    comment.save()
    data = {
    'pk': pk
        }
    return JsonResponse(data)

@login_required
def discussion_event_replies(request,pk):
    main_comment = Discussion_events.objects.get(pk=pk)
    user = request.user
    comments = Discussion_events.objects.filter(replied_to=main_comment)
    return render(request,'CodingClubIITG/reply_discussion_event.html',{'main_comment':main_comment,'comments':comments,'comment_id':pk,'user':user})

@login_required
def reply_comment_event(request,pk):
    comment = request.GET.get('comment')

    main_comment = Discussion_events.objects.get(pk=pk)
    event = main_comment.event
    d = Discussion_events(user=request.user,event=event,replied_to=main_comment,text=comment)
    d.save()
    return redirect('discussion_event_replies',pk)

# Projects


@login_required
def comment_project(request,pk):
    comment = request.GET.get('comment')

    project = Projects.objects.get(pk=pk)
    d = Discussion_projects(user=request.user,project=project,text=comment)
    d.save()
    return redirect('project_detail',pk)

@login_required
def delete_comment_project(request,pk):
    comment = Discussion_projects.objects.get(pk=pk)
    project_id = comment.project.pk
    comment.delete()
    return redirect('project_detail',project_id)

@login_required
def delete_reply_project(request,pk):
    comment = Discussion_projects.objects.get(pk=pk)
    comment_id = comment.replied_to.pk
    comment.delete()
    return redirect('discussion_project_replies',comment_id)

def edit_comment_project(request):
    pk = request.GET.get('pk')
    comment = Discussion_projects.objects.get(pk=pk)
    text = request.GET.get('inputValue')
    project_id = comment.project.pk
    comment.text = text
    comment.save()
    data = {
    'pk': pk
        }
    return JsonResponse(data)

@login_required
def discussion_project_replies(request,pk):
    main_comment = Discussion_projects.objects.get(pk=pk)
    user = request.user
    comments = Discussion_projects.objects.filter(replied_to=main_comment)
    return render(request,'CodingClubIITG/reply_discussion_project.html',{'main_comment':main_comment,'comments':comments,'comment_id':pk,'user':user})

@login_required
def reply_comment_project(request,pk):
    comment = request.GET.get('comment')

    main_comment = Discussion_projects.objects.get(pk=pk)
    project = main_comment.project
    d = Discussion_projects(user=request.user,project=project,replied_to=main_comment,text=comment)
    d.save()
    return redirect('discussion_project_replies',pk)
# ---------------------------------------------------------------------------------------------------------------------

# Feedback

@login_required
def feedback(request):
    user = request.user
    if request.method == 'POST':
        form = FeedbackForm(request.POST)

        if form.is_valid():
            mail_text = "Topic : " + form['topic'].value() + "\n" + form['feedback'].value() + "\n" + "From - " + user.username
            send_mail(
            'Feedback for codingclub website',
            mail_text,
            EMAIL_HOST_USER,
            ['codingclubiitg@gmail.com'],
            fail_silently = False
            )
            messages.success(request, f'Thanks for your valuable feedback/suggestion! We always try to give you the best.')
            return redirect('feedback')
        else:
            messages.error(request, f'There is an error.Please submit the form again.')
            return render(request,'CodingClubIITG/feedback.html',{'form':form })
    else:
        form = FeedbackForm(None)
        return render(request,'CodingClubIITG/feedback.html',{'form':form })
