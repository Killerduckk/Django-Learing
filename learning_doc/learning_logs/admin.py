from django.contrib import admin
from learning_logs.models import Topic,Entry,Writer,Image
# Register your models here.

# 在管理网址上注册Topic
admin.site.register(Topic)
admin.site.register(Entry)
admin.site.register(Writer)
admin.site.register(Image)