from django import forms   
from .models import Topic,Entry,Writer,Register_Writer

class TopicForm(forms.ModelForm):
    class Meta:
        model=Topic
        fields=['text']
        labels={'text':''}
       
        
class EntryFrom(forms.ModelForm):
    
    #FIXME：这几个属性是什么用处
    class Meta:
        model=Entry
        fields=['text']
        labels={'text':''}
        widgets={'text':forms.Textarea(attrs={'cols':80})}
        
class WriterForm(forms.ModelForm):
    class Meta:
        model=Writer
        fields=['name','password']
        labels={'name':'用户名','password':'密码'}
        widgets={'password':forms.PasswordInput()}
        
class RegisterForm(forms.ModelForm):
    class Meta:
        model=Register_Writer
        fields=['name','password','repassword']
        labels={'name':'用户名','password':'密码','repassword':'确认密码'}
        widgets={'password':forms.PasswordInput(),'repassword':forms.PasswordInput()}