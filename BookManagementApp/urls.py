from django.contrib import admin
from django.urls import path,include
from .views import * 

urlpatterns = [
    path('',home,name="home"),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('login/',home,name="login"),
    path('register/',register,name="register"),
    path('addnewstudent/',addnewstudent,name="addnewstudent"),
    path('addbook/',add_book,name="addbook"),
    path('book/<int:bookno>/delete/', deletebook, name='deletebook'),
    path('bookissued/<int:bookno>/delete/', deleteIssuedbook, name='deleteIssuedbook'),
    path('listbooks/',Listallbooks,name="listbooks"),
    path('issuebook/',IssueBook,name="issuebook"),
    path('returnbook/<int:id>',ReturnBooks,name="returnbook"),
    path('viewissuedbooks/',ViewIssuedBook,name="viewissuedbooks"),
    path('students/',Students,name="viewallstudents"),
    path('editstudent/<int:pk>',edit_student,name="editstudents"),
    path('students/<int:id>/delete/',deletestudent,name="deletestudent"),
    path('viewbooks/',ViewBooks,name="viewbooks"),
    path('profile/',profile,name="profile"),
    path('changepassword/',Changepassword,name="changepassword"),
    path("logout/", logoutview, name="logout"),
    path("books/", Books, name="books"),
    path("requestbooks/<int:id>", RequestBooks, name="requestbooks"),
    path("viewallrequests/", ViewAllRequests, name="viewallrequests"),
    path("acceptbookrequest/<int:id>", acceptBookRequest, name="acceptbookrequest"),
    path("rejectbookrequest/<int:id>", rejectBookRequest, name="rejectbookrequest"),
    path("getbook/<int:id>", getBook, name="getbook"),
    path("cancelrequest/<int:id>", cancelRequest, name="cancelrequest"),
    
]
