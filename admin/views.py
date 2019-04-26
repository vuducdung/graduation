from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

from admin.forms import ImageForm
from app.models import Accounts, Roles
from admin.models import *
from app.views import tran_word_search, get_categories, get_cuisines, get_districts
from django import forms
import json
from decouple import config


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user and user.is_active:
            # Redirecting to the required login according to user status.
            if user.role_id == 1:
                login(request, user)
                return redirect('/admin')
    return render(request, 'registration/login.html')


def location(request):
    if not request.user.is_authenticated or not request.user.role_id == 1:
        return redirect('/admin/login/')

    page = request.GET.get('page', 1)

    str1 = config('str1')
    str2 = config('str2')

    sql1 = "select admin_locations.* from admin_locations"
    sql2 = ' where True'

    username = request.GET.get('username', None)
    if username:
        query = tran_word_search(username, str1, str2)
        # query = query.replace(" ", ":*&")
        query_list = []
        for q in query.split(' '):
            q = q + ':*'
            query_list.append(q)
        query = "&".join(query_list)

        sql2 += " and news_tsv @@ to_tsquery('simple','" + query + "')"
        sql = sql1 + sql2
        locations = Locations.objects.raw(sql)
        paginator = Paginator(locations, 10)
        try:
            locations = paginator.page(page)
        except PageNotAnInteger:
            locations = paginator.page(1)
        except EmptyPage:
            locations = paginator.page(paginator.num_pages)
        return render(request, 'admin/location.html', {'locations': locations})
    avatar = None
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            avatar = uploadImage.objects.get(id=form.instance.id).image.url

    form = ImageForm()
    location_id = request.GET.get('id', None)
    delete = request.GET.get('delete', None)
    if delete:
        Locations.objects.filter(id=location_id).first().delete()
        return redirect('/admin/location/')

    if location_id:
        location = Locations.objects.filter(id=location_id).first()
        is_active = request.GET.get('is_active', None)
        if is_active:
            location.is_active = True
            require = RequireFromUser.objects.filter(location=location)
            if len(require) > 0:
                require[0].delete()
        nameLoc = request.GET.get('nameLoc', None)
        if nameLoc:
            location.name = nameLoc
        address = request.GET.get('address', None)
        if address:
            location.address = address
        time = request.GET.get('time', None)
        if time:
            location.workTime24h = time
        if avatar:
            location.avatar = avatar
        location.save()
        return render(request, 'admin/location.html',
                      {'location': location, 'form': form, 'avatar': avatar, })

    locations = Locations.objects.all().order_by('id')

    paginator = Paginator(locations, 10)
    try:
        locations = paginator.page(page)
    except PageNotAnInteger:
        locations = paginator.page(1)
    except EmptyPage:
        locations = paginator.page(paginator.num_pages)
    return render(request, 'admin/location.html', {'locations': locations})


def user(request):
    if not request.user.is_authenticated or not request.user.role_id == 1:
        return redirect('/admin/login/')

    user_id = request.GET.get('id', None)
    deactive = request.GET.get('deactive', None)
    active = request.GET.get('active', None)
    delete = request.GET.get('delete', None)

    if deactive and user_id:
        account = Accounts.objects.filter(id=user_id).first()
        account.is_active = False
        account.save()
        nickName = account.email.split("@")[0]
        return render(request, 'admin/user.html', {'account': account, 'nickName': nickName})

    if delete and user_id:
        account = Accounts.objects.filter(id=user_id).first()
        account.delete()
        # account.save()
        # nickName = account.email.split("@")[0]
        # return render(request, 'admin/user.html')
        return redirect('/admin/user/')

    if active and user_id:
        account = Accounts.objects.filter(id=user_id).first()
        account.is_active = True
        account.save()
        nickName = account.email.split("@")[0]
        return render(request, 'admin/user.html', {'account': account, 'nickName': nickName})

    if user_id:
        account = Accounts.objects.filter(id=user_id).first()
        nickName = account.email.split("@")[0]
        return render(request, 'admin/user.html', {'account': account, 'nickName': nickName})

    accounts = Accounts.objects.filter(role_id=2).order_by('id')
    page = request.GET.get('page', 1)
    paginator = Paginator(accounts, 10)
    try:
        accounts = paginator.page(page)
    except PageNotAnInteger:
        accounts = paginator.page(1)
    except EmptyPage:
        accounts = paginator.page(paginator.num_pages)

    return render(request, 'admin/user.html', {'accounts': accounts})


def index(request):
    if not request.user.is_authenticated or not request.user.role_id == 1:
        return redirect('/admin/login/')
    return render(request, 'admin/index.html')


def comment(request, id):
    location = Locations.objects.filter(id=id).first()
    page = request.GET.get('page', 1)
    username = request.GET.get('username', None)
    deleteId = request.GET.get('delete', None)
    # return HttpResponse({type(userId)})
    if deleteId:
        comment = CommentLikeShare.objects.get(id=deleteId)
        comment.delete()

    if username:
        try:
            users = Accounts.objects.filter(name__icontains=username).first()

            if users:
                comments = CommentLikeShare.objects.filter(location=location).filter(user=users).order_by('id')

                paginator = Paginator(comments, 10)
                try:
                    comments = paginator.page(page)
                except PageNotAnInteger:
                    comments = paginator.page(1)
                except EmptyPage:
                    comments = paginator.page(paginator.num_pages)
                return render(request, 'admin/comment.html', {'comments': comments})
        except:
            pass
    comments = CommentLikeShare.objects.filter(location=location).order_by('id')
    paginator = Paginator(comments, 10)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    return render(request, 'admin/comment.html', {'comments': comments})


def parking(request, id):
    location = Locations.objects.filter(id=id).first()
    page = request.GET.get('page', 1)
    # username = request.GET.get('username', None)
    deleteId = request.GET.get('delete', None)
    # return HttpResponse({type(userId)})
    if deleteId:
        parking = Parkings.objects.get(id=deleteId)
        parking.delete()

    parkings = location.parking.all()
    paginator = Paginator(parkings, 10)
    try:
        parkings = paginator.page(page)
    except PageNotAnInteger:
        parkings = paginator.page(1)
    except EmptyPage:
        parkings = paginator.page(paginator.num_pages)
    return render(request, 'admin/parking.html', {'parkings': parkings})


def add_location(request):
    hourL = ["%02d" % x for x in range(24)]
    minuteL = ["%02d" % x for x in range(60)]

    categories = get_categories()
    cuisines = get_cuisines()
    services = Services.objects.all()
    districts = get_districts()

    id_max = Locations.objects.order_by('-id').first().id + 1

    nameLoc = request.GET.get('nameLoc', None)
    if nameLoc:
        location = Locations()
        location.id = id_max
        location.name = nameLoc
        address = request.GET.get('address', None)
        location.address = address
        timeOpen1 = request.GET.get('timeOpen1', '00')
        timeOpen2 = request.GET.get('timeOpen2', '00')
        timeOpen = timeOpen1 + ':' + timeOpen2
        timeClose1 = request.GET.get('timeClose1', '00')
        timeClose2 = request.GET.get('timeClose2', '00')
        timeClose = timeClose1 + ':' + timeClose2
        location.workTime24h = timeOpen + ' - ' + timeClose
        description = request.GET.get('description', None)
        location.description = description
        latitude = request.GET.get('latitude', 0)
        location.latitude = latitude
        longitude = request.GET.get('longitude', 0)
        location.longitude = longitude

        str1 = config('str1')
        str2 = config('str2')
        
        location.url = tran_word_search(' '.join(location.name.lower().split(' ')), str1, str2).replace(' ', '-')
        exits_location = Locations.objects.filter(url=location.url)
        if len(exits_location) > 0:
            return HttpResponse('Địa điểm đã tồn tại')

        category = request.GET.get('category', None)
        category = Categories.objects.get(id=category)
        category_location = CategoryLocation()
        category_location.category = category
        category_location.location = location

        cuisine = request.GET.get('cuisine', None)
        cuisine = Cuisines.objects.get(id=cuisine)
        cuisine_location = CuisineLocation()
        cuisine_location.cuisine = cuisine
        cuisine_location.location = location

        district = request.GET.get('district', None)
        district = Districts.objects.get(id=district)
        location.district = district

        service = request.GET.get('service', None)
        service_location = ServiceLocation()
        ser = Services
        if service:
            ser = ser.objects.get(id=service)
            service_location.service = ser
            service_location.location = location

        location.save()
        service_location.save()
        cuisine_location.save()
        category_location.save()
        return redirect('/admin/location/?id=' + str(location.id))

    return render(request, 'admin/addLocation.html',
                  {'hourL': hourL, 'minuteL': minuteL, 'categories': categories,
                   'cuisines': cuisines, 'services': services, 'districts': districts,
                   }
                  )


def success(request):
    return HttpResponse('successfuly uploaded')


def get_required_message(request):
    if not request.user.is_authenticated or not request.user.role_id == 1:
        return redirect('/admin/login/')

    requires = RequireFromUser.objects.all()
    # location_deactive = Locations.objects.filter(is_active=False)
    messages = []
    if len(requires) > 0:
        for require in requires:
            required_user = require.user
            loc = require.location
            m = dict(userId=required_user.id, user_avatar=required_user.avatar, username=required_user.name,
                     loc_name=loc.name,
                     loc_id=loc.id, require_name=require.name, count=len(requires))
            messages.append(m)
    messages = json.dumps(messages)
    return HttpResponse(messages, content_type='application/json', )
