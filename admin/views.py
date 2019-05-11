from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

from admin.forms import ImageForm, MapForm, DishForm
from app.models import Accounts, Roles
from admin.models import *
from app.views import tran_word_search, get_categories, get_cuisines, get_districts, get_location_menu, \
    get_location_menu_v2, execute_word_search
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

    locationName = request.GET.get('location-name', None)
    if locationName:
        query = execute_word_search(locationName)
        if query:
            query = '&'.join(query)
            # query_list = []
            # for q in query.split(' '):
            #     q = q + ':*'
            #     query_list.append(q)
            # query = "&".join(query_list)

            sql2 += " and news_tsv @@ to_tsquery('" + query + "')"
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
    map = None
    if request.method == 'POST':
        image = request.FILES.get('image', None)
        map = request.FILES.get('map', None)

        form = ImageForm(request.POST, request.FILES)
        if form.is_valid() and image:
            if len(form.files) > 0:
                form.save()
                avatar = uploadImage.objects.get(id=form.instance.id).image.url

        form1 = MapForm(request.POST, request.FILES)
        if form1.is_valid() and map:
            if len(form1.files) > 0:
                form1.save()
                map = uploadMapImage.objects.get(id=form1.instance.id).map.url

    form = ImageForm()
    form1 = MapForm()
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
                notification = Notification()
                notification.user = require[0].user
                notification.location = location
                notification.content = "Bạn đã thêm địa điểm " + str(location.name) + " thành công"
                notification.save()
                require[0].delete()

        nameLoc = request.POST.get('nameLoc', None)
        if nameLoc:
            location.name = nameLoc
            str1 = config('str1')
            str2 = config('str2')
            location.url = tran_word_search(' '.join(location.name.lower().split(' ')), str1, str2).replace(' ', '-')
            exits_location = Locations.objects.filter(url=location.url)
            if len(exits_location) > 0:
                return HttpResponse('Tên địa điểm đã được sử dụng cho địa điểm khác')

        address = request.POST.get('address', None)
        if address:
            location.address = address
        time = request.POST.get('time', None)
        if time:
            location.workTime24h = time
        if avatar:
            location.avatar = avatar
        if map:
            location.map = map
        location.save()
        location.created_by = Accounts.objects.get(id=location.created_by)
        return render(request, 'admin/location.html',
                      {
                          'location': location, 'form': form,
                          'avatar': avatar, 'form1': form1
                      })

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

    user_name = request.GET.get('user-name', None)
    if user_name:
        accounts = Accounts.objects.filter(name__icontains=user_name).order_by('id')
        page = request.GET.get('page', 1)
        paginator = Paginator(accounts, 10)
        try:
            accounts = paginator.page(page)
        except PageNotAnInteger:
            accounts = paginator.page(1)
        except EmptyPage:
            accounts = paginator.page(paginator.num_pages)

        return render(request, 'admin/user.html', {'accounts': accounts})

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
    if not request.user.is_authenticated or not request.user.role_id == 1:
        return redirect('/admin/login/')

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
    if not request.user.is_authenticated or not request.user.role_id == 1:
        return redirect('/admin/login/')

    parking_id = request.GET.get('parking', None)
    if parking_id:
        parking = Parkings.objects.get(id=parking_id)
        return render(request, 'admin/parking.html', {'parking': parking})
    location = Locations.objects.filter(id=id).first()
    page = request.GET.get('page', 1)
    # username = request.GET.get('username', None)
    deleteId = request.GET.get('delete', None)
    # return HttpResponse({type(userId)})
    if deleteId:
        parking_location = ParkingLocation.objects.get(parking_id=deleteId, location_id=location.id)
        parking_location.delete()
        return redirect('/admin/location/' + str(location.id) + '/bai-do-xe/')

    parkings = location.parking.all()
    paginator = Paginator(parkings, 10)
    try:
        parkings = paginator.page(page)
    except PageNotAnInteger:
        parkings = paginator.page(1)
    except EmptyPage:
        parkings = paginator.page(paginator.num_pages)
    return render(request, 'admin/parking.html', {'parkings': parkings})


def get_menu_from_id(id):
    menu = Menus.objects.get(id=id)
    dishes = menu.dishes
    dishes = dishes.replace("'", '"')
    dishes = dishes.replace("False", "false")
    dishes = dishes.replace("None", "null")
    try:
        menu.dishes = json.loads(dishes)
        for dish in menu.dishes:
            if 'default' in str(dish['ImageUrl']):
                dish['ImageUrl'] = 'https://www.foody.vn/style/images/deli-dish-no-image.png'
            price = str(dish['Price']).replace('000.0', '.000')
            dish['Price'] = price
    except:
        return None
    return menu


def menu(request, id):
    if not request.user.is_authenticated or not request.user.role_id == 1:
        return redirect('/admin/login/')

    form = DishForm()
    menu_id = request.GET.get('menu_id', None)

    location = Locations.objects.filter(id=id).first()

    menu_name = request.POST.get('menu_name', None)
    if menu_name:
        menu_max_id = Menus.objects.all().order_by('-id')[0].id

        menu = Menus()
        menu.id = menu_max_id + 1
        menu.name = menu_name
        menu.save()
        menu_location = MenuLocation()
        menu_location.menu = menu
        menu_location.location = location
        menu_location.save()

        menus = get_location_menu_v2(location)
        if len(menus) <= 0:
            menus = None
        return render(request, 'admin/menus.html', {'menus': menus, 'form': form})

    create_dish_menu = request.POST.get('create_dish_menu', None)
    if create_dish_menu:
        menu = Menus.objects.get(id=create_dish_menu)
        name_dish = request.POST.get('name_dish', None)
        price_dish = request.POST.get('price_dish', None)
        form = DishForm(request.POST, request.FILES)
        if form.is_valid():
            if len(form.files) > 0:
                form.save()
                image = uploadDishImage.objects.get(id=form.instance.id).dish.url
                dish = Dish()
                dish.name = name_dish
                dish.price = price_dish
                dish.image = image
                dish.menu = menu
                dish.save()
                # menu = Menus.objects.get(id=create_dish_menu)
                return render(request, 'admin/menus.html', {'menu': menu, 'form': form})

    deleteId = request.GET.get('delete', None)
    # return HttpResponse({type(userId)})
    if deleteId and menu_id:
        menu = Menus.objects.get(id=menu_id)
        Dish.objects.get(id=deleteId).delete()
        return render(request, 'admin/menus.html', {'menu': menu, 'form': form})

    if menu_id:
        menu = Menus.objects.get(id=menu_id)
        return render(request, 'admin/menus.html', {'menu': menu, 'form': form})

    menus = get_location_menu_v2(location)
    if len(menus) <= 0:
        menus = None
    return render(request, 'admin/menus.html', {'menus': menus, 'form': form})


def add_location(request):
    if not request.user.is_authenticated or not request.user.role_id == 1:
        return redirect('/admin/login/')

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
        location.created_by = request.user.id

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
            service_location.save()

        location.save()

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


#
def sync(request):
    #     menus = Menus.objects.all()
    #
    #     for m in menus:
    #         menu = get_menu_from_id(m.id)
    #         if menu:
    #             for dish in menu.dishes:
    #                 price = int(float(dish['Price']))
    #                 name = dish['Name']
    #                 new_dish = Dish()
    #                 new_dish.price = price
    #                 new_dish.name = name
    #                 new_dish.menu = menu
    #                 new_dish.image = dish['ImageUrl']
    #                 new_dish.save()
    #
    return HttpResponse("EndSYNC")
