from django.shortcuts import render
from .models import Topic,Entry,Writer
from .froms import TopicForm,EntryFrom,WriterForm,RegisterForm
from django.http import HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
# Create your views here.

def index(request):
    """学习笔记的主页"""
    return render(request,'learning_logs/index.html')


def hello_world(request):
    return render(request,'learning_logs/hello_world.html')


def topics(request,writer_name): 
    print("!!!!!!!!!!!!!!!In function TOPICS:writer_name:"+writer_name)
    curr_writer=Writer.objects.filter(name=writer_name).first()
    topics=curr_writer.topics.order_by('date_added')
    print("topics:"+str(topics))
    context={'writer_name':writer_name,'topics':topics}   
    return render(request,'learning_logs/topics.html',context)

def topic(request,writer_name,topic_id):
    
    print("!!!!!!!!!!!!!!!In function TOPIC:topic_id:"+str(topic_id))
    curr_writer=Writer.objects.filter(name=writer_name).first()
    topic = Topic.objects.get(writer=curr_writer, id=topic_id)
    entries=topic.entries.order_by('-date_added')
    context={'writer_name':writer_name,'topic':topic,'entries':entries}   
    return render(request,'learning_logs/topic.html',context)


def new_topic(request,writer_name):
    print("!!!!!!!!!!!!!!!In function TOPICS:writer_name:"+writer_name)
    if request.method!='POST':
        form=TopicForm()
    else:
        form=TopicForm(request.POST)
        if form.is_valid():
            data=form.save(commit=False)    
            
            writer=Writer.objects.filter(name=writer_name).first()
            data.writer=writer
            data.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[writer_name,data.id]))     
    context={'form':form , 'writer_name':writer_name}
    return render(request,'learning_logs/new_topic.html',context)


def login(request):
    msg=""
    if request.method!='POST':
        form=WriterForm()
    else:
        form=WriterForm(request.POST)
        if form.is_valid():
            data=form.save(commit=False)
            data_in_db=Writer.objects.filter(name=data.name).first()
            #TODO:这里跳转到一个新的页面，再跳回来，实现错误处理
            if data_in_db is None:
                msg="用户名不存在,请重新输入"
            elif data_in_db.password!=data.password:
                msg="密码错误,请重新输入"
            elif data_in_db.password==data.password:
                 return HttpResponseRedirect(reverse('learning_logs:base',args=[data_in_db.name]))
    context={'form':form,'msg':msg}
    return render(request,'learning_logs/login.html',context)


def register(request):
    msg=""
    if request.method!='POST':
        form=RegisterForm()
    else:
        form=RegisterForm(request.POST)
        if form.is_valid():
            data=form.save(commit=False)
            data_in_db=Writer.objects.filter(name=data.name).first()
            if data.password!=data.repassword:
                msg="两次密码不一致,请重新输入"
            elif data_in_db is not None:
                msg="用户名已存在,请重新输入"
            elif data.password==data.repassword:
                 new_writer=Writer(name=data.name,password=data.password)
                 new_writer.save()
                 instructions=Topic(writer=new_writer,text="使用说明")
                 instructions.save()
                 instr_entry=Entry(topic=instructions,text=
                                   "你好{},欢迎使用学习笔记,在这里你可以创建你自己的文章,添加，编辑你的条目，快来使用吧！".format(new_writer.name))
                 instr_entry.save()
                 return HttpResponseRedirect(reverse('learning_logs:base',args=[new_writer.name]))
    context={'form':form,'msg':msg}
    return render(request,'learning_logs/register.html',context)


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
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[writer_name,topic_id]))
    print("In func new_entry topic_id:"+str(topic_id))
    context={'form':form,'topic':topic,'writer_name':writer_name,}
    return render(request,'learning_logs/new_entry.html',context)
      
    

