from django.shortcuts import render
from .models import Topic,Entry,Writer,Image,Favorite
from .froms import TopicForm,EntryFrom,WriterForm,RegisterForm,LoginForm
from django.http import HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db.models import Count
from django.http import HttpResponse
import os
# Create your views here.

def index(request):
    """学习笔记的主页"""
    return render(request,'learning_logs/index.html')


def hello_world(request):
    return render(request,'learning_logs/hello_world.html')


def topics(request,writer_name):
    curr_writer=Writer.objects.filter(name=writer_name).first()
    topics=curr_writer.topics.order_by('date_added')
    print("topics:"+str(topics))
    context={'writer_name':writer_name,'topics':topics}   
    return render(request,'learning_logs/topics.html',context)

def topic(request,viewer_name,topic_id,sort_type):
    topic = Topic.objects.get(id=topic_id)
    viewer=Writer.objects.filter(name=viewer_name).first()
    entries=topic.entries.order_by('-date_added')
    favor=topic.favor_topics.filter(lover=viewer).first()
    favor_num=topic.favor_topics.count()
    is_favor=True
    if favor is None:
        is_favor=False
    context={'viewer_name':viewer_name,'topic':topic,'entries':entries,"is_favor":is_favor,
             "favor_num":favor_num,"sort_type":sort_type}
    print("viewer_name:"+viewer_name)
    return render(request,'learning_logs/topic.html',context)


def new_topic(request,writer_name):
    if request.method!='POST':
        form=TopicForm()
    else:
        form=TopicForm(request.POST)
        if form.is_valid():
            data=form.save(commit=False)    
            
            writer=Writer.objects.filter(name=writer_name).first()
            data.writer=writer
            data.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[writer_name,data.id,'new']))
    context={'form':form , 'writer_name':writer_name}
    return render(request,'learning_logs/new_topic.html',context)


def login(request):
    msg=""
    if request.method!='POST':
        form=LoginForm()
    else:
        form=LoginForm(request.POST)
        if form.is_valid():
            data=form.save(commit=False)
            data_in_db=Writer.objects.filter(name=data.name).first()
            #TODO:这里跳转到一个新的页面，再跳回来，实现错误处理
            if data_in_db is None:
                msg="用户名不存在,请重新输入"
            elif data_in_db.password!=data.password:
                msg="密码错误,请重新输入"
            elif data_in_db.password==data.password:
                 return HttpResponseRedirect(reverse('learning_logs:profile',args=[data_in_db.name]))
    context={'form':form,'msg':msg}
    return render(request,'learning_logs/login.html',context)


def register(request):
    msg=""

    #预先存贮的头像图片
    try:
        default_avatar = Image.objects.get(id=1)
        print("default_avatar is exist")
    except ObjectDoesNotExist:
        print("default_avatar not exist")
        default_avatar = None
    if request.method!='POST':
        form=WriterForm()
    else:
        form=WriterForm(request.POST, request.FILES)
        if form.is_valid():
            data=form.save(commit=False)
            data_in_db=Writer.objects.filter(name=data.name).first()
            if data.password!=data.repassword:
                msg="两次密码不一致,请重新输入"
            elif data_in_db is not None:
                msg="用户名已存在,请重新输入"
            elif data.password==data.repassword:
                 #处理图片

                 new_writer=form.save()
                 instructions=Topic(writer=new_writer,text="你好{}，这是我们为你准备的使用说明".format(new_writer.name))
                 instructions.save()

                 instr_entry=Entry(topic=instructions,text=
                                   "你好{},欢迎使用学习笔记,在这里你可以创建你自己的文章,添加，编辑你的条目，还可以阅览其他用户创建的优秀文章，"
                                   "快来体验吧！".format(new_writer.name))
                 instr_entry.save()

                 return HttpResponseRedirect(reverse('learning_logs:profile',args=[new_writer.name]))
    context={'form':form,'msg':msg,'default_avatar':default_avatar}
    return render(request,'learning_logs/register.html',context)


def profile(request,writer_name):
    curr_writer=Writer.objects.filter(name=writer_name).first()
    context={'writer_name':writer_name,'writer':curr_writer}
    return render(request,'learning_logs/profile.html',context)

def base(request,writer_name):
    context={'writer_name':writer_name}
    return render(request,'learning_logs/base.html',context)

def new_entry(request,writer_name,topic_id):
    curr_writer=Writer.objects.filter(name=writer_name).first()
    topic=Topic.objects.get(writer=curr_writer,id=topic_id)
    if request.method!='POST':
        form=EntryFrom()
    else:
        form=EntryFrom(data=request.POST)
        if form.is_valid():
            new_entry=form.save(commit=False)
            new_entry.topic=Topic.objects.get(id=topic_id)
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[writer_name,topic_id,'new']))
    print("In func new_entry topic_id:"+str(topic_id))
    context={'form':form,'topic':topic,'writer_name':writer_name,}
    return render(request,'learning_logs/new_entry.html',context)

def forum(request,viewer_name,order_type='new'):
    me=Writer.objects.filter(name=viewer_name).first()
    print("me:"+str(me))
    sorted_topics=Topic.objects.exclude(writer=me).order_by('-date_added')
    for topic in sorted_topics:
        if "这是我们为你准备的使用说明" in topic.text:
            sorted_topics=sorted_topics.exclude(id=topic.id)
    if order_type=='hot':
        sorted_topics=sorted_topics.annotate(num_entries=Count('entries')).order_by('-num_entries')
    elif order_type=='favorite':
        sorted_topics=sorted_topics.annotate(num_favorites=Count('favor_topics')).order_by('-num_favorites')
    context={'viewer_name':viewer_name,'topics':sorted_topics,'order_type':order_type}
    return render(request,'learning_logs/forum.html',context)


def my_favor(request,viewer_name,order_type='new'):
    me=Writer.objects.filter(name=viewer_name).first()

    topics = me.lovers.all().values_list('topic', flat=True)
    #直接排序？
    sorted_topics=Topic.objects.filter(id__in=topics).order_by('-date_added')
    if order_type=='hot':
        sorted_topics=sorted_topics.annotate(num_entries=Count('entries')).order_by('-num_entries')
    elif order_type=='favorite':
        sorted_topics=sorted_topics.annotate(num_favorites=Count('favor_topics')).order_by('-num_favorites')
    context={'viewer_name':viewer_name,'topics':sorted_topics,'order_type':order_type}
    return render(request,'learning_logs/my_favor.html',context)

def toggle_favorite(request,viewer_name,topic_id,page_type='forum'):
    topic=Topic.objects.get(id=topic_id)
    me=Writer.objects.filter(name=viewer_name).first()
    new_favor=me.lovers.filter(lover=me,topic=topic)
    msg=""
    if new_favor:
        print("已经取消收藏")
        new_favor.delete()
        msg="已经取消收藏"
    else:
        print("已经收藏")
        my_new_favor=Favorite(lover=me,topic=topic)
        my_new_favor.save()
        msg="已经收藏"
    context={'viewer_name':viewer_name,'topic':topic,'msg':msg,'page_type':page_type}
    return render(request,'learning_logs/favor_msg.html',context)

def topic_writer_profile(request,viewer_name,topic_id):
    topic=Topic.objects.get(id=topic_id)
    writer=topic.writer
    topics=writer.topics.all()
    context={'viewer_name':viewer_name,'writer':writer,'topics':topics}
    return render(request,'learning_logs/topic_writer_profile.html',context)




