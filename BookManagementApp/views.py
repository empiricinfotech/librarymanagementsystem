from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import *
from django.db.models import Q
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
# Create your views here.

User = get_user_model()

def validate_password_strength(password):
    if len(password) < 8:
        raise ValidationError("Password must contain at least 8 characters.")

    if not any(char.isupper() for char in password):
        raise ValidationError("Password must contain at least one uppercase letter.")

    if not any(char.islower() for char in password):
        raise ValidationError("Password must contain at least one lowercase letter.")

    if not any(char.isdigit() for char in password):
        raise ValidationError("Password must contain at least one digit.")

    validate_password(password)
    return True

def home(request):
    if request.method == 'POST':
        username = request.POST['email']
        pwd = request.POST['password']
        user = authenticate(email=request.POST['email'],password = request.POST['password'])
        if user:
            login(request, user)
            if request.user.is_superuser:
                return redirect("/addbook")
            return redirect('viewbooks')
        return render(request,"login.html",{"alert":"Invalid Credentials"})
    return render(request,"login.html")

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        fnm = request.POST['firstname']
        lnm = request.POST['lastname']
        username = request.POST['username']
        pwd = request.POST['password']
        conpwd = request.POST['confirmpassword']
        try:
            validate_password_strength(pwd)
        except ValidationError as e:
            messages.error(request, e.message)
            return render(request,'register.html',{"alert":e.message})
        if pwd == conpwd:
            user = User.objects.filter(email = email)
            if not user:
                user = User.objects.create_user(email=email,username=username,password=pwd,first_name=fnm,last_name=lnm)
                return redirect("profile")     
    return render(request,'register.html')

def addnewstudent(request):
    if request.method == 'POST':
        email = request.POST['email']
        fnm = request.POST['firstname']
        lnm = request.POST['lastname']
        username = request.POST['username']
        pwd = request.POST['password']
        user = User.objects.filter(email = email)
        if not user:
            user = User.objects.create_user(email=email,username=username,password=pwd,first_name=fnm,last_name=lnm)
            return redirect("viewallstudents")     
    return render(request,'addNewStudent.html')

@login_required
def add_book(request):
    if request.user.is_superuser:
        if request.method == "POST":
            book_name = request.POST["bookname"]
            author_name = request.POST["author"]
            book_publication = request.POST["bookpublisher"]
            book_id = request.POST["bookno"]
            book_qty = request.POST["bookqty"]
            book = Book.objects.filter(bookNo=book_id).exists()
            if not book:
                book = Book.objects.create(name=book_name,author=author_name,bookNo=book_id,publication=book_publication,qty=book_qty,available_qty=book_qty)
                context = {
                    "id":book,
                    "bookname":book.name
                }
                return render(request,"create_Book.html",{"alert":"Book Added Successfully"})
            else:
                return render(request,"create_Book.html",{"alert":"Unique Book Number already Exists"})
        return render(request,"create_Book.html")
    return redirect('login')

@login_required
def deletebook(request,bookno):
    if request.user.is_superuser:
        book = get_object_or_404(Book, pk=bookno)
        book.delete()
        return redirect('listbooks')
    return redirect('login')
    
@login_required
def Listallbooks(request):
    if request.user.is_superuser:
        books = Book.objects.all()
        if request.method == "GET":
            return render(request,"list_of_books.html",{"book":books})
        if request.method == "POST":
            book = Book.objects.get(pk=request.POST['bookid'])
            bookname = request.POST['booknm']
            authorname = request.POST['authornm']
            bookno = request.POST['booknumber']
            qty = request.POST['qtys']
            book.name = bookname
            book.author = authorname
            book.bookNo = bookno
            book.qty = qty
            book.available_qty = (int(book.qty) - book.issued_qty)
            book.save()
            return render(request,"list_of_books.html",{"book":books})
    else:
        return redirect('login')
        
@login_required  
def IssueBook(request):
    if request.user.is_superuser:
        users = User.objects.filter(is_active = True)
        books = Book.objects.all()
        if request.method == 'POST':
            usr = request.POST['userselect']
            req_book = request.POST['bookselect']
            user = User.objects.get(email=usr)
            book = Book.objects.get(bookNo=req_book)
            if book.available_qty != 0:
                filteredbook = IssuedBook.objects.filter(book=book,user=user)
                if filteredbook.filter(status="Issued"): 
                    return render(request,"issue_a_book.html",{"users":users,"books":books,'alert':f'Book already Issued To {usr} First Return A Book'})
                else:
                    IssuedBook.objects.create(user=user,book=book)
                    book.issued_qty += 1
                    book.available_qty -= 1
                    book.save() 
                    return render(request,"issue_a_book.html",{"users":users,"books":books,'alert':"Book Issued"})
            else:
                return render(request,"issue_a_book.html",{"users":users,"books":books,"alert":"Book currently not available"})
        return render(request,"issue_a_book.html",{"users":users,"books":books})
    return redirect('login')

@login_required
def ViewIssuedBook(request):
    if request.user.is_superuser:
        books = IssuedBook.objects.filter(status="Issued")
        return render(request,"view_all_Issued_books.html",{"book":books})
    return redirect('login')

@login_required
def Students(request):
    if request.user.is_superuser:
        student = User.objects.filter(is_superuser = False,is_active = True)
        return render(request,"list_of_students.html",{"students":student})
    return redirect('login')

@login_required
def deletestudent(request,id):
    if request.user.is_superuser:
        user = get_object_or_404(User, pk=id)
        book_issues = IssuedBook.objects.filter(user=id)
        for book_issue in book_issues:
            if book_issue.status == "Issued":
                book_issue.status = "Return"
                book_issue.save()
                book = book_issue.book
                book.available_qty = F("available_qty") + 1
                book.issued_qty = F("issued_qty") - 1 
                book.save()                                                                          
        user.is_active = False
        user.save()
        return redirect('viewallstudents')
    return redirect('login')

@login_required  
def deleteIssuedbook(request, bookno):
    if request.user.is_superuser:
        book = get_object_or_404(IssuedBook, pk=bookno)
        book.delete()
        books = book.book
        books.available_qty += 1
        books.issued_qty -= 1
        books.save()
        return redirect('viewissuedbooks')
    return redirect('login')

@login_required
def profile(request):
    if request.method == "GET":
        user = request.user
        return render(request,"profile.html",{"user":user})
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.save()
        return render(request,"profile.html",{"user":user})  
     
@login_required   
def edit_student(request,pk):
    if request.user.is_superuser:
        user = User.objects.get(id=pk)
        if request.method == "POST":
            email = user.email
            usernm = user.username
            users_query = User.objects.exclude(Q(email=email),Q(username=usernm))
            email_already_exists = users_query.filter(email=request.POST['email']).exists()
            username_already_exists = users_query.filter(username=request.POST['username']).exists()
            if email_already_exists:
                return render(request,"editstudent.html",{'user': user,'alert':"Email Address Already Exists"})
            if username_already_exists:
                return render(request,"editstudent.html",{'user': user,'alert':"UserName Already Exists"}) 
            user = User.objects.get(id=pk)
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            username = request.POST['username']
            email = request.POST['email']
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.save()
            return redirect('viewallstudents')
        else:
            return render(request,"editstudent.html",{'user': user})
    return redirect('login')
@login_required  
def logoutview(request):
    logout(request)
    return redirect("login")

@login_required
def Changepassword(request):
    user = request.user
    if request.method == 'POST':
        if user.check_password(request.POST['currentpassword']):
            if request.POST['newpassword'] == request.POST['confirmpassword']:
                user.set_password(request.POST['newpassword'])
                user.save()
                return render(request,"change_password.html",{"alert":"Password Changed Successfully"})
            return render(request,"change_password.html",{"alert":"Password And Confirm Password Not matched"})
        return render(request,"change_password.html",{"alert":"Please Input Correct Current Password"})
    return render(request,"change_password.html")

@login_required
def ViewBooks(request):
    books = IssuedBook.objects.filter((Q(user = request.user)&Q(status = "Return") )| (Q(user = request.user)&Q(status = "Issued")))
    return render(request,"Issued_book.html",{"book":books})

@login_required
def ReturnBooks(request,id):
    books = IssuedBook.objects.get(pk = id)
    issued_date = books.issued_date
    if books.status == "Issued":
        books.status = "Return"
        books.issued_date = issued_date
        books.expiry_date = None
        books.save()
        book = books.book
        book.available_qty = F('available_qty') + 1
        book.issued_qty = F('issued_qty') - 1
        book.save()
    return redirect('viewissuedbooks')

@login_required
def Books(request):
    if not request.user.is_superuser:
        books = Book.objects.filter(available_qty__gt=0).exclude(id__in=(IssuedBook.objects.filter(Q(user=request.user)&Q(status='Issued'))).values('book'))
        requestedBooks = Book.objects.filter(id__in = IssuedBook.objects.filter(Q(user=request.user)&Q(status='Requested')).values('book'))
        return render(request,"studentRequestBook.html",{"book":books,"requested":requestedBooks})
    return redirect('login')

@login_required
def RequestBooks(request,id):
    book = Book.objects.get(id=id)
    IssuedBook.objects.create(user=request.user,book = book,status="Requested",expiry_date=None,issued_date=None)
    return redirect('books')

@login_required
def ViewAllRequests(request):
    if request.user.is_superuser:
        books = IssuedBook.objects.filter(status = "Requested")
        return render(request,"viewAllRequest.html",{"book":books})
    return redirect('login')

@login_required
def acceptBookRequest(request,id):
    if request.user.is_superuser:
        books = IssuedBook.objects.get(pk = id)
        if books.status == "Requested":
            books.status = "Issued"
            books.issued_date = datetime.datetime.today()
            books.expiry_date = datetime.datetime.today() + timedelta(days=14)
            books.save()
            book = books.book
            book.available_qty = F('available_qty') - 1
            book.issued_qty = F('issued_qty') + 1
            book.save()
        return redirect('viewallrequests')
    return redirect('login')

@login_required
def rejectBookRequest(request,id):
    if request.user.is_superuser:
        books = IssuedBook.objects.get(pk = id)
        if books.status == "Requested":
            books.delete()
        return redirect('viewallrequests')
    return redirect('login')


def getBook(request,id):
    abc = list(Book.objects.filter(pk = id).values())
    return JsonResponse(abc, safe=False)

@login_required
def cancelRequest(request,id):
    if not request.user.is_superuser:
        demo  = IssuedBook.objects.filter(Q(user = request.user) & Q(book = id) & Q(status = "Requested"))
        if demo:
            demo.delete()
            return redirect('books')
    return redirect('login')