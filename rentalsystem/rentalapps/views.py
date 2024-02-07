from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login,logout
from .models import customusers
from datetime import datetime
from .models import Car,customusers
from .models import Booking
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
# Create your views here.


# ///////////////////// main index pages /////////////////////////
def index(request):
    cars = Car.objects.all().order_by('-price')
    return render(request, 'index.html',{'cars':cars,})


def user_register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']
        password = request.POST['password']
        if customusers.objects.filter(username=username).exists():
            return render(request,'register.html',{'message':'username already exists'})
        if customusers.objects.filter(email=email).exists():
            return render(request,'register.html',{'message':'email already exists'})
        
        user = customusers.objects.create_user(username=username,first_name=first_name,last_name=last_name,user_type="user",email=email,address=address,
                                              phone=phone,password=password)
        user.save()
        # return redirect()
        return redirect(user_login)
    else:
        return render(request, 'register.html')


def company_register(request):
    if request.method == 'POST':
        company_name = request.POST['companyname']
        username = request.POST['username']
        company_address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        location = request.POST['location']
        password = request.POST['password']
        if customusers.objects.filter(username=username).exists():
            return render(request,'company_register.html',{'message':'username already exists'})
        if customusers.objects.filter(email=email).exists():
            return render(request,'company_register.html',{'message':'email already exists'})
        data = customusers.objects.create_user(company_name=company_name,address=company_address,location=location,user_type="company",phone=phone,username=username,
                                               email=email,password=password)
        data.save()
        return HttpResponse("company register successful")
    else:

        return render(request,'company_register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        admin_user = authenticate(request, username=username, password=password)
        if admin_user is not None and admin_user.is_staff:
            login(request,admin_user)
            return redirect('admin:index')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            if user.user_type == "company":# company has logined
                return redirect(view_car)
            elif user.user_type == "user":# coutsomuser has has logined
                return redirect(userindex)
        else:
            return render(request, 'login.html',{'message':'Invalid Login Credentials'})

    return render(request, 'login.html')  


def userlogout(request):
    auth.logout(request)
    return redirect(index)



# ///////////////////// company  pages /////////////////////////

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def bookings(request):
    return render(request, 'company/booking.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def add_car(request):
    user = customusers.objects.get(id=request.user.id)
    if request.method == 'POST':
        name = request.POST['name']
        car_model = request.POST['car_model']
        price = request.POST['price']
        image = request.FILES['image']
        details = request.POST['details']
        new_car = Car.objects.create(company_id=user,name=name, car_model=car_model, price=price, details=details,image=image)
        new_car.save()
        # return HttpResponse('Car added successfully')
        return redirect(view_car)
    else:
        return render(request, 'company/addcar.html',)
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def edit_car(request,id):
    user = customusers.objects.get(id=request.user.id)
    car = Car.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST['name']
        car_model = request.POST['car_model']
        price = request.POST['price']
        details = request.POST['details']
        car.name=name
        car.car_model=car_model
        car.details=details
        car.price=price
        car.save()
        return redirect(view_car)
    else:
        return render(request,'company/edit.html',{'data':car})


@login_required(login_url=user_login)    
def update_company(request):
    user = customusers.objects.get(id=request.user.id)
    if request.method == 'POST':
        company_name = request.POST['company_name']
        address = request.POST['company_address']
        location = request.POST['location']
        data = customusers.objects.update(company_name=company_name,
            address=address,
            location=location
    )
        return HttpResponse('Update successful')
    else:

        return render(request, 'company/update.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def view_car(request):           
    user = customusers.objects.get(id=request.user.id)
    data = Car.objects.filter(company_id=user.id)
    items_per_page = 5
    # Use Paginator to paginate the products
    paginator = Paginator(data, items_per_page)
    page = request.GET.get('page', 1)
    try:
        cars = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        cars = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver the last page of results
        cars = paginator.page(paginator.num_pages)
    return render(request, 'company/carview.html', {'data': cars})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def car_status(request,id):
    car = Car.objects.get(id=id)
    if request.method == 'POST':
        status = request.POST['status']
        car.status = status
        car.save()
        return redirect(view_car)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def view_requests(request):
    user = customusers.objects.get(id=request.user.id)
    print(user)
    datas = Car.objects.filter(company_id=user.id)
    print(datas)
    all_bookings = Booking.objects.filter(car__in=datas)
    return render(request, 'company/review.html',{'all_bookings': all_bookings})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def statusrequest(request,id):
    datas = Booking.objects.get(id=id)
    car = Car.objects.get(id=datas.car.id)
    if request.method == 'POST':
        booking = request.POST['booking']
        if booking == 'accepted':
            datas.status = 'approved'
            car.status = "Unavailable"

        elif booking == 'reject':
            datas.status = 'rejected'
        
        datas.save()
        car.save()
    return redirect(view_requests)

@login_required(login_url=user_login)
def delete(request,id):
    user = customusers.objects.get(id=request.user.id)
    user = Car.objects.filter(id=id)

    user.delete()
    return redirect(view_car)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def history(request):
    user = customusers.objects.get(id=request.user.id)
    data = Car.objects.filter(company_id = user.id)
    datas = Booking.objects.filter(status='paid',car__in=data)
    items_per_page = 5
    # Use Paginator to paginate the products
    paginator = Paginator(datas, items_per_page)
    page = request.GET.get('page', 1)
    try:
        bookings = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        bookings = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver the last page of results
        bookings = paginator.page(paginator.num_pages)
    return render(request, 'company/history.html', {'all_bookings': bookings})


# ///////////////////// user pages /////////////////////////

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def user_requests(request):
    user = customusers.objects.get(id=request.user.id)
    all_bookings = Booking.objects.filter(user=user).order_by('status')
    items_per_page = 5
    # Use Paginator to paginate the products
    paginator = Paginator(all_bookings, items_per_page)
    page = request.GET.get('page', 1)
    try:
        bookings = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        bookings = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver the last page of results
        bookings = paginator.page(paginator.num_pages)
    return render(request, 'user/viewrequest.html',{'all_bookings': bookings})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def userindex(request):
    cars = Car.objects.all().order_by('-price')
    return render(request, 'user/userindex.html',{'cars': cars})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def cars(request):           
    user = customusers.objects.get(id=request.user.id)
    print(user)
    data = Car.objects.all()
    print(data)
    return render(request, 'user/cars.html', {'data': data})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def booking(requset):
    if requset.method == 'POST':
        user = requset.POST['user']
        no_of_days = requset.POST['no_of_days']
        day = requset.POST['day']
        Total_cost = requset.POST['Total_cost']
        booking_date = requset.POST[' booking_date']
        status = requset.POST['status']
        Bookings = Booking.objects.create(user=user,no_of_days=no_of_days,day=day,Total_cost=Total_cost,booking_date=booking_date,status='pending')
        Bookings.save()
        return HttpResponse('Booking successful')
    else:
        return render(requset, 'user/booking.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def profile(request):
    data = customusers.objects.get(id=request.user.id)
    return render(request, 'user/profile.html', {'data': data})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def edit_profile(request,id):
    users = customusers.objects.get(id=request.user.id)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']
        data = customusers.objects.update(first_name=first_name,last_name=last_name,email=email,phone=phone,
                            address=address)
        return redirect(profile)
    else:
        return render(request, 'user/editprofile.html',{'users':users})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def view_users(request):
    data = customusers.objects.get(id=request.user.id)
    print(data.first_name)
    return render(request, 'user/userview.html', {'data': data})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def car_request(request, id):
    user = customusers.objects.get(id=request.user.id)
    car = Car.objects.get(id=id)
    today = timezone.now().strftime("%Y-%m-%d")
    if request.method == 'POST':
        no_of_days = int(request.POST['no_of_day'])
        day = request.POST['day']
        num = no_of_days * car.price

        booking_request = Booking.objects.create(
            user=user,
            car=car,
            no_of_days=no_of_days,
            starting_day=day,
            Total_cost=num,
        )                                                                     
        booking_request.save()

        return redirect(user_requests)
    
    else:
        return render(request,'user/request.html',{'car': car, 'today':today})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def car_details(request,id):
    if request.method == 'GET':
        car = Car.objects.get(id=id)
        return render(request,'user/car-details.html',{'car':car})


def car_search(request):
    if request.method == "GET":
        car_name = request.GET['car_name']
        data = Car.objects.filter(name__icontains=car_name)
        return render(request, 'user/cars.html', {'data': data})
    else:
        return render(request, 'user/cars.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def user_history(request):
    user = customusers.objects.get(id=request.user.id)
    bookings = Booking.objects.filter(user=user)
    items_per_page = 5
    # Use Paginator to paginate the products
    paginator = Paginator(bookings, items_per_page)
    page = request.GET.get('page', 1)
    try:
        bookings = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        bookings = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver the last page of results
        bookings = paginator.page(paginator.num_pages)
    data = customusers.objects.all()
    return render(request, 'user/userhistory.html',{'all_bookings':bookings})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def update_status(request, id):
    booking = Booking.objects.get(id=id)

    if request.method == 'POST':
        booking.status = 'paid'
        
        booking.save()

        return redirect(user_requests)
    else:
        return render(request, 'user/payment.html', {'a': booking})
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def review_add(request,id):
    data = Booking.objects.get(id=id)
    print(data)
    if request.method == 'POST':
        review  = request.POST['review']   
        Rating = request.POST['rating']

        data.review = review
        data.Rating = Rating

        data.save()

        return redirect(user_requests)
    else:
        return render(request,'viewrequest.html',{'datas':data})
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=user_login)
def booking_review(request):
    datas = Booking.objects.all() 
    return render(request, 'user/cars.html', {'datas': datas})