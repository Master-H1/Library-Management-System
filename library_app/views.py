from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.db.models import Count
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User, Group, auth
from django.http import HttpResponseRedirect
from . import forms
from .models import Books, StudentExtra, BookCategory, IssueBooktoStudent, BorrowBookModel, Chatroom
from django.contrib import messages
from datetime import datetime, timedelta, date
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
# exporting to pdf document
from django.template.loader import get_template

# ==========================================================================
# voice recognition

# =====================================================================


def HomePage(request):
    user = User.objects.all()
    context = {'user': user}
    return render(request, 'index.html', context)

# Users choose where to login


def UsersLoginPage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterLogi')
    return render(request, 'userLogin.html')

# Librarian Sign up part


def AdminPartSignup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exist')
                return redirect('studentclick')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email taken')
                return redirect('studentclick')
            else:
                stud = User.objects.create_user(
                    username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                stud.save()
                my_student_group = Group.objects.get_or_create(
                    name='LIBRARIAN')
                my_student_group[0].user_set.add(stud)
                if True:
                    messages.success(
                        request, "Account created successfully!!!")
                    return redirect('AdminLogi')
        else:
            messages.error(request, "Password doesn't match")
            return redirect('adminclick')
    return render(request, 'adminSignup.html')

# student Sign up part


def StudentPartSignup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        school = request.POST['school']
        department = request.POST['department']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exist')
                return redirect('studentclick')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email taken')
                return redirect('studentclick')
            else:
                stud = User.objects.create_user(
                    username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                stud.save()
                my_student_group = Group.objects.get_or_create(name='STUDENT')
                my_student_group[0].user_set.add(stud)

                user = auth.authenticate(username=username, password=password1)
                if user is not None:
                    auth.login(request, user)

                studextra = StudentExtra.objects.create(
                    student=request.user,
                    school=school,
                    department=department
                )
                studextra.save()
                if True:
                    messages.success(
                        request, "Account created successfully!!!")
                    return redirect('afterLogi')
        else:
            messages.error(request, "Password doesn't match")
            return redirect('studentclick')
    return render(request, 'studentSignup.html')


def is_admin(user):
    return user.groups.filter(name='LIBRARIAN').exists()


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

# this is the view for page of after admin login and dashboard


def afterLogin_view(request):
    page11 = "Dashboard"

    if is_admin(request.user):
        return render(request, 'adminAfterlogin.html', {'page11': page11})

    elif is_student(request.user):
        page11 = "Dashboard"
        stud = StudentExtra.objects.get(student=request.user.id)
        context = {'page11': page11, 'stud': stud}
        return render(request, 'studentAfterlogin.html', context)
    else:
        return redirect('admin')

# student updating the profile


def stupdateProfile(request):
    page11 = "Dashboard"

    if is_admin(request.user):
        for1 = User.objects.get(id=request.user.id)
        form1 = forms.userUpdateForm(instance=for1)
        if request.method == 'POST':
            form1 = forms.userUpdateForm(request.POST, instance=for1)
            if form1.is_valid():
                form1.save()
                if True:
                    messages.success(
                        request, 'Your Profile updated Successfully!!!')
                    return redirect('afterLogi')
        context = {'form1': form1, 'page11': page11}
        return render(request, 'adminAfterlogin.html', context)

    elif is_student(request.user):
        page11 = "Dashboard"
        for1 = User.objects.get(id=request.user.id)
        form1 = forms.userUpdateForm(instance=for1)

        for2 = StudentExtra.objects.get(student=for1)
        form2 = forms.StudentExtraUpdateForm(instance=for2)
        if request.method == 'POST':
            form1 = forms.userUpdateForm(request.POST, instance=for1)
            form2 = forms.StudentExtraUpdateForm(
                request.POST, request.FILES, instance=for2)

            if form1.is_valid() and form2.is_valid():
                form1.save()
                form2.save()
                if True:
                    messages.success(
                        request, 'Your Profile updated Successfully!!!')
                    return redirect('afterLogi')
        context = {'form1': form1, 'form2': form2, 'page11': page11}
        return render(request, 'studentAfterlogin.html', context)

    else:
        return redirect('admin')
# =========================================


def logoutPage(request):
    logout(request)
    return redirect('home')
# View Part of seeing availabe book in libray
# books


def BooksRoom_view(request):

    categories = BookCategory.objects.all()
    allbooks = Books.objects.all()

    CATID = request.GET.get("categories")
    if CATID:
        allbooks = Books.objects.filter(category=CATID)

    else:
        allbooks = Books.objects.all()
    context = {'allbooks': allbooks, 'categories': categories}
    return render(request, 'Books.html', context)

# details of book displayed on template


def Book_detail_view(request, pk):
    allbook = Books.objects.get(id=pk)
    content = {'allbook': allbook}
    return render(request, 'book-detail.html', content)

# student borrow or request a book


@login_required(login_url="studLogin")
@user_passes_test(is_student)
def BorrowBook_view(request, pk):
    BorrowBookModel.objects.all()
    stud = StudentExtra.objects.get(student=request.user.id)
    allbook = Books.objects.get(id=pk)
    borform = forms.BorrowBookForm()
    if request.method == 'POST':
        reque = BorrowBookModel.objects.filter(book=allbook).exists()
        if reque:
            messages.error(
                request, 'Opps!!! This book already requested by other student, you can request another other wait for the day this one will be avilbable!')
            context = {'borform': borform, 'allbook': allbook, 'stud': stud}
            return render(request, 'borrowbook.html', context)
        BorrowBookModel.objects.get_or_create(
            student=stud,
            book=allbook
        )
        borform = forms.BorrowBookForm(request.POST)
        if borform.is_valid():
            borform.save(commit=False)
            if True:
                return redirect('Bookrequested')
    context = {'borform': borform, 'allbook': allbook, 'stud': stud}
    return render(request, 'borrowbook.html', context)


# add book to library
@login_required(login_url='adminlogi')
@user_passes_test(is_admin)
def addBookToLibrary(request):
    page2 = "adBo"
    addbooks = forms.BooksForm()
    if request.method == 'POST':
        addbooks = forms.BooksForm(request.POST, request.FILES or None)
        if addbooks.is_valid():
            addbooks.save()
            messages.success(request, 'Book added Successfully!!!')
            return redirect('addedto')
    context = {'page2': page2, 'addbooks': addbooks}
    return render(request, 'adminAfterlogin.html', context)

# books added to library message


def bookaddedToLibrary(request):
    page222 = "addedto"
    return render(request, 'adminAfterlogin.html', {'page222': page222})

# Updating or edit book in library


@login_required(login_url='adminlogi')
@user_passes_test(is_admin)
def updateBook(request, pk):
    page22 = "EditBo"
    book = Books.objects.get(id=pk)
    addbooks = forms.BooksForm(instance=book)
    if request.method == 'POST':
        addbooks = forms.BooksForm(request.POST, request.FILES, instance=book)
        if addbooks.is_valid():
            addbooks.save()
            return redirect('availableBo')
    context = {'page22': page22, 'addbooks': addbooks}
    return render(request, 'adminAfterlogin.html', context)

# deleting a book in library


@login_required(login_url='adminlogi')
@user_passes_test(is_admin)
def deleteBook(request, pk):
    book = Books.objects.get(id=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('availableBo')
    return render(request, 'delete.html', {'obj': book})

# View Part of seeing availabe book in libray


@login_required(login_url='adminlogi')
@user_passes_test(is_admin)
def AvailableBooks(request):
    page3 = "availableBo"
    avaibook = Books.objects.all()
    context = {'page3': page3, 'avaibook': avaibook}
    return render(request, 'adminAfterlogin.html', context)

# View Part of giving a book  availabe book in libray to student


@login_required(login_url='adminlogi')
@user_passes_test(is_admin)
def IssueBook(request):
    page4 = "isuBo"
    form = forms.IssuedBookForm()
    if request.method == 'POST':
        form = forms.IssuedBookForm(request.POST)
        if form.is_valid():
            form.save()
            # here we will save book issued to sudent
            messages.success(request, 'Book issued to student successfully!')
            return redirect('viewissued')
    context = {'page4': page4, 'form': form}
    return render(request, 'adminAfterlogin.html', context)

# view books issued to student seen by Librarian


@login_required(login_url='adminlogi')
@user_passes_test(is_admin)
def viewissuedbook_view(request):
    page44 = "viewissued"
    issuedbooks = IssueBooktoStudent.objects.all()
    context = {'page44': page44, 'issuedbooks': issuedbooks}
    return render(request, 'adminAfterlogin.html', context)
# This will remove student on the list of those who borrowed the books


def Removestusentfromborrow(request, pk):
    remove = IssueBooktoStudent.objects.get(id=pk)
    if request.method == 'POST':
        remove.delete()
        return redirect('viewissued')
    return render(request, 'delete.html', {'obj': remove})

# view student who bellong to our System using librarian panel


@login_required(login_url='adminlogi')
@user_passes_test(is_admin)
def viewstudent_view(request):
    page5 = "viewStud"
    students = StudentExtra.objects.all()
    context = {'students': students, 'page5': page5}
    return render(request, 'adminAfterlogin.html', context)

# View books issued to student


@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    pageSTUD1 = "Studbissue"
    stud = StudentExtra.objects.get(student=request.user)
    issuedbook = IssueBooktoStudent.objects.filter(student=stud)
    context = {'pageSTUD1': pageSTUD1, 'issuedbook': issuedbook}
    return render(request, 'studentAfterlogin.html', context)

# The books requested by student to borrow


def BookstudentRequested(request):
    BorrowBookModel.objects.all()
    if is_admin(request.user):
        page55 = "Bookreq"
        reques = BorrowBookModel.objects.all()
        context = {'reques': reques, 'page55': page55}
        return render(request, 'adminAfterlogin.html', context)
    elif is_student(request.user):
        page55 = "Bookreq"
        stud = StudentExtra.objects.get(student=request.user.id)
        reques = BorrowBookModel.objects.filter(student=stud)
        context = {'page55': page55, 'reques': reques}
        return render(request, 'studentAfterlogin.html', context)

# accept or issue a book which a student requested to borrow


def acceptStudent_request(request, pk):
    page6 = "acceptBo"
    accept = BorrowBookModel.objects.get(id=pk)
    if request.method == 'POST':
        issue = IssueBooktoStudent.objects.filter(book=accept.book).exists()
        if issue:
            messages.warning(
                request, 'This book already issued to other!, you can let him/her to be on waiting list or cancel request!')
            context = {'page6': page6, 'accept': accept}
            return render(request, 'adminAfterlogin.html', context)
        issue = IssueBooktoStudent.objects.create(
            student=accept.student,
            book=accept.book,
            status=accept.statusoption
        )
        issue.save()
        accept.delete()
        return redirect('viewissued')
    context = {'page6': page6, 'accept': accept}
    return render(request, 'adminAfterlogin.html', context)
# cancel book request


def CancelBookRequested(request, pk):
    cancel = BorrowBookModel.objects.get(id=pk)
    if request.method == 'POST':
        cancel.delete()
        return redirect('Bookrequested')
    return render(request, 'delete.html', {'obj': cancel})

# about our website


def about_view(request):
    return render(request, 'about.html')

# courses learning or view part


def courses_view(request):
    return render(request, 'video-detail.html')

# our contact page


def contact_view(request):
    if request.method == 'POST':
        message_name = request.POST['name']
        message_email = request.POSTT['email']
        message = request.POST['message']
        send_mail(
            message_name,  # subject
            message,  # body
            message_email,  # from
            ['merchiorabawee@gmail.com'],
        )
    return render(request, 'contact.html')

  # chat with librarian or students


def Chat(request):
    rooms = Chatroom.objects.all()
    participants = User.objects.all()
    num = participants.count()
    use = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        message = request.POST.get('message')
        chat = Chatroom.objects.create(
            user=use,
            message=message
        )
        chat.save()
        if True:
            return redirect('chat')
    context = {'rooms': rooms, 'participants': participants, 'num': num}
    return render(request, 'chat/friend.html', context)

# ==================================================================================================
# Books reading summary


def bar_chart_view(request):
    # Retrieve data from the model
    data = IssueBooktoStudent.objects.values(
        'status').annotate(count=Count('status'))

    # Prepare data for chart.js
    labels = [item['status'] for item in data]
    counts = [item['count'] for item in data]

    # Generate data for chart.js
    chart_data = {
        'labels': labels,
        'datasets': [{
            'label': 'Book Counts',
            'data': counts,
            'backgroundColor': ['red', 'green', 'blue', 'yellow'],
        }]
    }

    return render(request, 'report/chart.html', {'chart_data': chart_data})


# pie chart
def pie_chart_view(request):
    # Retrieve data from the model
    data = IssueBooktoStudent.objects.values(
        'status').annotate(count=Count('status'))

    # Prepare data for chart.js
    labels = [item['status'] for item in data]
    counts = [item['count'] for item in data]

    # Generate data for chart.js
    chart_data = {
        'labels': labels,
        'datasets': [{
            'data': counts,
            'backgroundColor': ['red', 'green', 'blue', 'yellow'],
        }]
    }

    return render(request, 'report/pie_chart.html', {'chart_data': chart_data})
# =============================================================================================
# ============================================================================================
# Exporting to pdf


def exportpdf_view(request):
    # Retrieve the data from the model
    data = IssueBooktoStudent.objects.all()

    # Load the template
    template = get_template('report/export.html')

    # Render the data
    context = {'data': data}
    rendered_template = template.render(context)

    # Create a PDF object
    pdf = HttpResponse(content_type='application/pdf')
    pdf['Content-Disposition'] = 'attachment; filename="Library Management week Summary Report.pdf"'

    # Convert the HTML template into PDF
    pisa_status = pisa.CreatePDF(rendered_template, dest=pdf)

    # If PDF generation failed, return an error
    if pisa_status.err:
        return HttpResponse('PDF creation error')

    return pdf
