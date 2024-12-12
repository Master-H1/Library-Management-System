from django.db import models
from django.contrib.auth.models import User,AbstractUser
from datetime import timedelta , datetime,date,time
from django.utils.timezone import now
# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Department(models.Model):
    school = models.ForeignKey(School,db_column="school",on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class StudentExtra(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profiles',default='profiles/profile.png',null=True,blank=True)
    school = models.CharField(max_length=200,null=True)
    department = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.student.first_name

    @property
    def get_name(self):
        return self.student.first_name
    @property
    def getuserid(self):
        return self.student.id
    
class BookCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Books(models.Model):
    category = models.ForeignKey(BookCategory,db_column="category",on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='books_img')
    name = models.CharField(max_length=100)
    isbn=models.PositiveIntegerField()
    description = models.TextField()
    author = models.CharField(max_length=100)
    published = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-published',]
        verbose_name_plural = "Books"
    
def get_expiry():
    return datetime.today() + timedelta(days=2)

class IssueBooktoStudent(models.Model):
 
    student = models.ForeignKey(StudentExtra,db_column='student',on_delete=models.CASCADE)
    book = models.OneToOneField(Books,db_column='book',on_delete=models.CASCADE)
    issuedate = models.DateField(auto_now=True)
    expiredate = models.DateField(default=get_expiry)
    fines = models.IntegerField(default=0)
    status = models.CharField(max_length=100,null=True)

    def get_fines(self):
        if self.expiredate is not None and self.issuedate is not None:
            issuedate_datetime = datetime.combine(self.issuedate, time.min)
            expiredate_datetime = datetime.combine(self.expiredate, time.min)
            days = (expiredate_datetime - issuedate_datetime).days
            fine = max(days - 2, 0) * 10
            return fine
        return 0

    def save(self, *args, **kwargs):
        self.fine = self.get_fines()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.book.name} issued to {self.student.student.first_name}"
        
    class Meta:
        ordering = ['-issuedate',]
    

class BorrowBookModel(models.Model):
    status = (
        ('Borrow','Borrow'),
         )
    student = models.ForeignKey(StudentExtra,db_column='student',on_delete=models.CASCADE)
    book = models.OneToOneField(Books,db_column='book',on_delete=models.CASCADE)
    statusoption = models.CharField(max_length=100,choices=status,default="Borrow")
    borrowdate = models.DateField(auto_now=True)
    
    def __str__(self):
        return f"'{self.book.name}'  requested by  '{self.student.student.first_name}'"

class Borrowbooksummary(models.Model):
    status = (
        ('Available','Availabe'),
        ('Borrowed','Borrowed'),
        ('Returned','Returned'),
        ('Not Available','Not Available'),

    )
    student = models.ForeignKey(to=StudentExtra,db_column='student',on_delete=models.CASCADE)
    book = models.ForeignKey(to=Books,db_column='book',on_delete=models.CASCADE)
    status = models.CharField(max_length=100,null=True,choices=status)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.student.student.first_name
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Borrowbooksummary"

class Chatroom(models.Model):
    user = models.ForeignKey(to=User,db_column='user',on_delete=models.CASCADE)
    message = models.TextField()
    timesend = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.user.student.first_name


