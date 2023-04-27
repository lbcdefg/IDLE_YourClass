from django import forms
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget

# 글쓰기에서(자료실이 아닌 일반게시판) Post 객체 생성을 위한 폼
class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
 
        fields = ['title', 'category', 'body', 'post_fix'] 
        
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width: 80%', 'placeholder': '제목을 입력하세요.', 'title':'제목'}
            ),
            'category': forms.Select(
                attrs={'class': 'custom-select'},
            ),
            'body': forms.CharField(widget=CKEditorUploadingWidget()),
            'file': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width: 80%', 'placeholder': '파일경로를 입력하세요(기능구현전)'}
            ),
            'post_fix':forms.CheckboxInput(),
        }
        labels = {
            'title' : '글제목',
            'category' :'게시판',
            'body' : '내용',
            'post_fix' : '공지로 설정',  
        }

# 글 상세보기에서 Comment 객체 생성을 위한 폼      
class PostCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
 
        fields = ['comment_text']
        widgets = {
            'comment_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 30})
        }
        
# 게시판관리에서 Categories 객체 생성을 위한 폼
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        
        fields = ['Cat_name', 'Cat_info']
        
        labels = {
            'Cat_name' : '게시판 이름',
            'Cat_info' : '게시판 설명',
        }
        
        widgets = {
            'Cat_name': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width: 60%', 'placeholder': '게시판 이름을 입력하세요'}
            ),
            
            'Cat_info': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width: 60%', 'placeholder': '게시판에 대해 간단하게 설명해주세요'}
            ),
        }

# 게시판관리에서 Categories 객체 수정을 위한 폼
class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Categories
        
        fields = ['Cat_info']
        
        labels = {
            'Cat_info' : '게시판 설명',
        }
        
        widgets = {
            'Cat_info': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width: 60%', 'placeholder': '게시판에 대해 간단하게 설명해주세요'}
            ),
        }
        
# 캘린더 생성을 위한 폼
class EventForm(forms.ModelForm):
  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats parses HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

# 자료실 파일 업로드와 글쓰기 폼
from django_summernote.widgets import SummernoteWidget

class PostWriteForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'file']
        widgets = {
            'body': SummernoteWidget(),
        }
        labels = {
            'title' : '글제목',
            'body' : '내용',
        }
