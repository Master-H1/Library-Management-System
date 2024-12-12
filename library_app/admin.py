from django.contrib import admin
from library_app.models import School,StudentExtra,Department,Books,BookCategory,IssueBooktoStudent,BorrowBookModel,Borrowbooksummary,Chatroom
# Register your models here.
@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    ordering =('name',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name','school')
    ordering = ('name',)

@admin.register(StudentExtra)
class StudentExtraAdmin(admin.ModelAdmin):
    list_display = ('student','department','school')

admin.site.register(BookCategory)

class BooksAadmin(admin.ModelAdmin):
    list_display = ('name','isbn','author','published',)
    search_fields =('name','isbn','author','published',)
    list_per_page =5
admin.site.register(Books,BooksAadmin)

admin.site.register(IssueBooktoStudent)
admin.site.register(BorrowBookModel)
admin.site.register(Borrowbooksummary)
admin.site.register(Chatroom)

