from django.shortcuts import render
from django_email_verification import send_email
from .forms import UserRegistrationForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404,  HttpResponseRedirect
from django.contrib.auth import get_user_model
from .models import Book, Percent
from django.views.generic import ListView

def user_signup(request):
    form = UserRegistrationForm(request.POST, use_required_attribute=False)
    n = 0
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.email = form.cleaned_data.get('email')
        user.save()
        user.is_active = False
        send_email(user)
        return render(request, 'notification.html', {'notification': "На вашу почту отправленно письмо, перейдите по ссылке для завершения регистрации"})
    else:
        n = n + 1

    return render(request, 'signup.html', {'form': form, 'n': n})

def user_logout(request):
    logout(request)
    return redirect('/login')

def user_login(request):
    k = 0
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/my_books')
            else:
                k = 1
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'k': k})

def book_view(request, id):
    book = Book.objects.get(id=id)
    if request.user.is_authenticated:
        if request.method == "POST":
            default_percent = Percent.objects.get(book=book, user=request.user)
            form_percent = request.POST.get('percent', '')
            speed_name = request.POST.get('speed_select')
            print(speed_name)
            if speed_name == 'Медленная скорость':
                speed_select = 200
            elif speed_name == 'Быстрая скорость':
                speed_select = 600
            else:
                speed_select = 350
            if (form_percent != '') or (form_percent != default_percent):
                Percent.objects.filter(book=book, user=request.user).update(percent=form_percent)
            start_performing = True
        else:
            speed_select = 350
            if Percent.objects.filter(user=request.user, book=book).exists():
                percent = Percent.objects.get(book=book, user=request.user)
                start_performing = False
            else:
                percent = Percent()
                percent.book = book
                percent.user = request.user
                percent.percent = 0
                percent.save()
                start_performing = False

        percent = Percent.objects.get(book=book, user=request.user)

        text = book.text
        number_symbols_to_delete = len(text) * int(percent.percent) * 0.01
        text = text[int(number_symbols_to_delete):]
        return render(request, 'book.html', {'book': book, 'percent': percent, 'start_performing': start_performing, 'text': text, 'speed_select': speed_select})
    else:
        percent = 0
        start_performing = False
        return render(request, 'book.html', {'book': book, 'percent': percent, 'start_performing': start_performing})

def index(request):
    return render(request, 'index.html')

def catalog(request):
    book_list = Book.objects.filter(public_active=True, public=True)
    return render(request, 'catalog.html', {'book_list': book_list})

def book_addition(request, id):
    book = get_object_or_404(Book, id=id)
    if book.additions.filter(id=request.user.id).exists():
        book.additions.remove(request.user)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        book.additions.add(request.user)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

def new_book(request):
    if request.method == "POST":
        title = request.POST.get('title', "")
        author = request.POST.get('author', "")
        book_image = request.FILES['book_image']
        public_active = request.POST.get('public_active')
        if public_active == 'on':
            public_active = True
        else:
            public_active = False
        gendre = request.POST.get('gendre')
        book_file = request.FILES.get('book_file', '')
        if book_file != '':
            text = book_file.read().decode("utf-8")
            text = text[2:-1]
        else:
            text = request.POST.get('book_text', "")
        new_book = Book()
        print(text)
        new_book.creator = request.user
        new_book.title = title
        new_book.author = author
        new_book.text = text
        new_book.book_image = book_image
        new_book.public = public_active
        new_book.gendre = gendre
        new_book.save()
        return redirect('/my_books')

    return render(request, 'new_book.html')

def my_books(request):
    book_list = Book.objects.filter(creator=request.user) | Book.objects.filter(additions=request.user)
    return render(request,
                  'my_books.html',
                  {'book_list': book_list})

class Search(ListView):
    template_name = 'catalog.html'
    model = Book

    def get_queryset(self):
        return Book.objects.filter(title__icontains=self.request.GET.get("q").title())

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q").title()}&'
        return context