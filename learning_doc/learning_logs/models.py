from django.db import models

# Create your models here.

class Register_Writer(models.Model):
    name=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    repassword=models.CharField(max_length=200)
    def __str__(self):
        return self.name


class Writer(models.Model):
    name=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    def __str__(self):
        return self.name

    @classmethod
    def get_default_writer(cls):
        return cls.objects.get(name="wgy")


class Topic(models.Model):
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE, null=True,related_name='topics')
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        if self.writer is None:
            self.writer = Writer.get_default_writer()
        super().save(*args, **kwargs)
# 条目
class Entry(models.Model):
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE,related_name='entries')
    text = models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)
#FIXME：没有理解Meta的用法
    class Meta: 
        verbose_name_plural='entries'
    
    def __str__(self):
        return self.text[:50]+"..."
    
