from django.urls import re_path
from django.urls import path

from . import views


urlpatterns = [
    re_path('^addprojects/$', views.addProjects, name = 'addprojects'),
    re_path('^addevents/$', views.addEvents, name = 'addevents'),
    re_path('^$', views.index, name='index'),
    re_path('^aboutus/$', views.aboutus, name='aboutus'),
    re_path('^blog/$', views.blog, name='blog'),
    re_path('^events/$', views.events, name='events'),
    re_path('^projects/$', views.projects, name='projects'),
    # path('logout/', views.logout, name='logout'),
    re_path('^eventdescription/<int:pk>$', views.event_template, name='event_template'),
    path("projects/<int:pk>", views.project_detail, name="project_detail"),
    path("events/<int:pk>", views.event_detail, name="event_detail"),

    # New additions

    # Favorites
    path('events/favorite_event/', views.favorite_event, name='favorite_event'),
    path('events/unfavorite_event/', views.unfavorite_event, name='unfavorite_event'),
    path('events/unfavorite_event_all/', views.unfavorite_event_all, name='unfavorite_event_all'),

    path('projects/favorite_project/', views.favorite_project, name='favorite_project'),
    path('projects/unfavorite_project/', views.unfavorite_project, name='unfavorite_project'),
    path('projects/unfavorite_project_all/', views.unfavorite_project_all, name='unfavorite_project_all'),

    # Discussion Forum

    # Events
    path('events/discussion_event_replies/<int:pk>', views.discussion_event_replies, name='discussion_event_replies'),

    path('events/comment_event/<int:pk>', views.comment_event, name='comment_event'),
    path('events/reply_comment_event/<int:pk>', views.reply_comment_event, name='reply_comment_event'),

    path('events/delete_comment_event/<int:pk>', views.delete_comment_event, name='delete_comment_event'),
    path('events/delete_reply_event/<int:pk>', views.delete_reply_event, name='delete_reply_event'),
    path('events/edit_comment_event/', views.edit_comment_event, name='edit_comment_event'),

    # Projects
    path('projects/discussion_project_replies/<int:pk>', views.discussion_project_replies, name='discussion_project_replies'),

    path('projects/comment_project/<int:pk>', views.comment_project, name='comment_project'),
    path('projects/reply_comment_project/<int:pk>', views.reply_comment_project, name='reply_comment_project'),

    path('projects/delete_comment_project/<int:pk>', views.delete_comment_project, name='delete_comment_project'),
    path('projects/delete_reply_project/<int:pk>', views.delete_reply_project, name='delete_reply_project'),
    path('projects/edit_comment_project/', views.edit_comment_project, name='edit_comment_project'),

    # Feedback
    path('feedback', views.feedback, name='feedback'),


]
