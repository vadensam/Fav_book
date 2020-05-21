from django.shortcuts import render, redirect
from .models import User,Book
import bcrypt
from django.contrib import messages


def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User.objects.create(
        fname = request.POST['fname'],
        lname = request.POST['lname'],
        email = request.POST['email'],
        password = pw_hash,
    )
    request.session['id'] = user.id
    return redirect('/success')

def login(request):
    user_db = User.objects.filter(email=request.POST['email'])
    if user_db:
        log_user = user_db[0]

        if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
            request.session['id'] = log_user.id
            return redirect('/success')

    messages.error(request, 'Incorrect email or password.')
    return redirect('/')

def success(request):
    user = User.objects.get(id=request.session['id'])
    context = {
        'user' : user,
        'all_books' : Book.objects.all(),
        'all_users' : User.objects.all(),
    }
    return render(request, 'user.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def add_book(request):
    user = User.objects.get(id=request.session['id'])
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/success')

    book = Book.objects.create(
        title = request.POST['title'],
        desc = request.POST['desc'],
        user = user
    )
    book.fav_users.add(user)
    return redirect('/success')

def view_book(request, book_id):
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['id'])
    if book not in user.books.all():
        return redirect(f'/display/{book.id}')
    context = {
        'book' : book,
        'user' : user
    }
    return render(request, 'edit.html', context)

def update(request):
    book = Book.objects.get(id=request.POST['book_id'])
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/books/{book.id}')

    book.title = request.POST['title']
    book.desc = request.POST['desc']
    book.save()
    return redirect(f'books/{book.id}')

def delete(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('/success')    

def display(request, book_id):
    book = Book.objects.get(id=book_id)
    context ={
        'book' : book,
        'user' : User.objects.get(id=request.session['id'])
    }
    return render(request, 'display.html', context)

def add_fav(request, book_id):
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['id'])
    book.fav_users.add(user)
    return redirect(f'/books/{book.id}')

def unfav(request, book_id):
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['id'])
    user.fav_books.remove(book)
    return redirect(f'/books/{book.id}')