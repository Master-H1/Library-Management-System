from django import forms
from django.contrib.auth.models import User
from .models import StudentExtra,Books,IssueBooktoStudent,BorrowBookModel

class StudentExtraForm(forms.ModelForm):
    class Meta:
        model = StudentExtra
        fields = ['school','department']

        widgets={
            'school':forms.Select(attrs={'style': 'width:250px; border-radius:5px'}),
            'department':forms.Select(attrs={'style':'width:250px; border-radius:5px'}),
        }
class userUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','username','email']

class StudentExtraUpdateForm(forms.ModelForm):
    class Meta:
        model = StudentExtra
        fields = ['photo','school','department']

class BooksForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['photo','name','isbn','description','author','category']

        widgets = {
            'description':forms.Textarea(attrs={'style':'width:200px;'}),
            'category':forms.Select(attrs={'style':'width:200px;'})
        }

class IssuedBookForm(forms.ModelForm):
    class Meta:
        model = IssueBooktoStudent
        fields = ['student','book','status']

        widgets = {
            'student':forms.Select(attrs={'style':'width:200px;'}),
            'book':forms.Select(attrs={'style':'width:200px;'}),
        }
class BorrowBookForm(forms.ModelForm):
    class Meta:
        model = BorrowBookModel
        fields = ['statusoption',]
    
    widgets = {
        'statusoption':forms.Select(attrs={'style':'width:300px;'})
    }