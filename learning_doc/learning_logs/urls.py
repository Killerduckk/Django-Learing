from django.conf.urls import url
from . import views
#FIXME :别忘记.表示当前目录

urlpatterns=[
    #FIXME :r'^$'表示空字符串
    url(r'^index/$',views.index,name='index'),
    #实现多级路由 localhost:8000/fir/helloworld
    url(r'^helloworld/$',views.hello_world,name='hello_world'),
    
    url(r'^topics/(?P<writer_name>\w+)/$',views.topics,name='topics'),
    #TODO： :r'^$'表示空字符串
    # 不可以多级别吗？
    url(r'^topics/(?P<viewer_name>\w+)/(?P<topic_id>\d+)/$',views.topic,name='topic'),
    
    url(r'^new_entry/(?P<writer_name>\w+)/(?P<topic_id>\d+)/$',views.new_entry,name='new_entry'),
   
    url(r'^new_topic/(?P<writer_name>\w+)/$',views.new_topic,name='new_topic'),
    
    url(r'^login/$',views.login,name='login'),
    
    url(r'^$',views.login,name='login'),
    
    
    url(r'^register/$',views.register,name='register'),
        
    url(r'^base/(?P<writer_name>\w+)$',views.base,name='base'),


    url(r'^profile/(?P<writer_name>\w+)/$',views.profile,name='profile'),

    url(r'^forum/(?P<viewer_name>\w+)/(?P<order_type>\w+)/$',views.forum,name='forum'),

    url(r'^toggle_favorite/(?P<viewer_name>\w+)/(?P<topic_id>\d+)/(?P<page_type>\w+)/$',views.toggle_favorite,name='toggle_favorite'),


    url(r'^my_favor/(?P<viewer_name>\w+)/(?P<order_type>\w+)/$',views.my_favor,name='my_favor')

]