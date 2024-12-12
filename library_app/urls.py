from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('',views.HomePage,name='home'),
    #----voice recognition
    
    # Other URL patterns for your website
    path('admin/',views.afterLogin_view,name='admin'),
    path('userLogin',views.UsersLoginPage,name='userLG'),
    path('accounts/login/',LoginView.as_view(template_name='login.html')),
   
    #admin accessbility
    path('Adminclick/',views.AdminPartSignup,name='adminclick'),
    path('AdminLogin/',LoginView.as_view(template_name='adminLogin.html'),name='AdminLogi'),

    #student accessibility
    path('Studentclick/',views.StudentPartSignup,name='studentclick'),
    path('StudentLogin/',LoginView.as_view(template_name='studentLogin.html'),name='studLogin'),
    path('accounts/profile/',views.afterLogin_view,name='afterLogi'),
    path('Studentupdate',views.stupdateProfile,name='stupdate'),
    path('StudentViewhisbooks',views.viewissuedbookbystudent,name='Studbissue'),
    path('Borrowb/<str:pk>',views.BorrowBook_view,name='Borb'),
    path('Bookrequested',views.BookstudentRequested,name='Bookrequested'),
    path('cancelBookrequested/<str:pk>',views.CancelBookRequested,name='cancelrequested'),
    
    #All operations related to librarian
    path('Books/',views.BooksRoom_view,name='Books'),
    path('BookDetails/<str:pk>',views.Book_detail_view,name='bookdV'),
    path('Dashboard/',views.afterLogin_view,name='Dashboard'),
    path('adBo/',views.addBookToLibrary,name='adBo'),
    path('Added/',views.bookaddedToLibrary,name='addedto'),
    path('EditBo/<str:pk>',views.updateBook,name='EditBo'),
    path('Delet/<str:pk>',views.deleteBook,name='Delet'),
    path('availableBo/',views.AvailableBooks,name="availableBo"),
    path('isuBo/',views.IssueBook,name='isuBo'),
    path('viewissued/',views.viewissuedbook_view,name='viewissued'),
    path('remstudentfrombor/<str:pk>',views.Removestusentfromborrow,name='remb'),
    path('Viewstudent/',views.viewstudent_view,name='viewStud'),
    path('AcceptStudentreq/<str:pk>',views.acceptStudent_request,name='AcceptStudentreq'),

    #other parts for menu bar
    path('accounts/logout/',views.logoutPage,name='logout'),
    path('Videos/',views.courses_view,name='vid'),
    path('AboutV/',views.about_view,name='about'),
    path('Contacts/',views.contact_view,name='contact'),
    # chat whith other students or librarian
    path('Chatwithstud/',views.Chat,name='chat'),

   #looks for summary report
    path('bar_chart_view/', views.bar_chart_view, name='bar_chart_view'),
    path('pie_chart_view/', views.pie_chart_view, name='pie_chart_view'),
    # ...
    # Exporting to pfd
    path('exportpdf/', views.exportpdf_view, name='topdf'),
    # ...
]       