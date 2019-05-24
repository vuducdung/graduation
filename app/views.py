from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
import ast
from app.models import *
from admin.models import *
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token, account_reset_token
from django.contrib.auth import get_user_model
import json
import re
from decouple import config
from django.db import connection

from django.core.mail import EmailMessage

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.utils.dateparse import parse_datetime
from datetime import datetime


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            # return HttpResponse(current_site.domain)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'id': user.id,
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, id, token):
    try:
        # uid = id
        User = get_user_model()
        user = User.objects.get(id=id)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is None:
        return HttpResponse('No user!')
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def resetRequire(request):
    if request.method == 'GET':
        email = request.GET.get('email', None)
        if email:
            User = get_user_model()
            user = User.objects.filter(email=email)
            if len(user) > 0:
                user = user[0]
                current_site = get_current_site(request)
                mail_subject = 'Reset your account.'
                message = render_to_string('reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'id': user.id,
                    'token': account_reset_token.make_token(user),
                })
                emails = EmailMessage(
                    mail_subject, message, to=[email]
                )
                emails.send()
                return HttpResponse('Please confirm your email address to complete the reset password')
            else:
                return render(request, 'registration/resetRequire.html', {'message': 'Account not found'})
    return render(request, 'registration/resetRequire.html')


def reset(request, id, token):
    if request.method == 'POST':
        p1 = request.POST.get('pass1', None)
        p2 = request.POST.get('pass2', None)
        User = get_user_model()
        user = User.objects.get(id=id)
        if p1 and p2:
            if p1 == p2:
                user.set_password(p1)
                user.save()
                # return render(request, 'registration/login.html', {reset: True})
                return redirect('/login/', {'reset': True})
            else:
                return render(request, 'reset_form.html', {'message': 'Hai mat khau khop'})
    return render(request, 'reset_form.html')


def get_locations():
    locations = Locations.objects.filter(is_active=True).order_by('-totalView') \
                    .only("id", "name", "address", "avatar", "description")[:40]
    return locations


def get_location_by_url(locationUrl):
    url = locationUrl
    loc = Locations.objects.filter(url=url).filter(is_active=True).first()
    if loc:
        evaluation = loc.evaluation
        evaluation = evaluation.replace('[', '').replace(']', '').replace("'", "")
        # evaluation = [i.strip(' ') for i in evaluation]
        loc.evaluation = evaluation.split(',')[1:6]
        loc.evaluation = [i.strip(' ') for i in loc.evaluation]
        totalReview = 0
        avgRating = 0
        if loc.avgRating:
            avgRating = loc.avgRating
        if loc.totalReview:
            totalReview = loc.totalReview
        point = float(avgRating) * float(totalReview)
        point_1 = float(loc.evaluation[0]) * float(totalReview)
        point_2 = float(loc.evaluation[1]) * float(totalReview)
        point_3 = float(loc.evaluation[2]) * float(totalReview)
        point_4 = float(loc.evaluation[3]) * float(totalReview)
        point_5 = float(loc.evaluation[4]) * float(totalReview)
        new_reviews = CommentLikeShare.objects.filter(location=loc).filter(type_id=1).filter(
            created_at__range=(parse_datetime('2019-04-20 20:48:17.099000'), datetime.now()))
        if len(new_reviews) > 0:
            for re in new_reviews:
                point += float(re.score)
                review_list = re.evaluation.split(',')
                point_1 += float(review_list[0])
                point_2 += float(review_list[1])
                point_3 += float(review_list[2])
                point_4 += float(review_list[3])
                point_5 += float(review_list[4])
            loc.avgRating = round(float(point) / int(len(new_reviews) + int(totalReview)), 1)
            loc.evaluation = [
                round(float(point_1) / int(len(new_reviews) + int(totalReview)), 1),
                round(float(point_2) / int(len(new_reviews) + int(totalReview)), 1),
                round(float(point_3) / int(len(new_reviews) + int(totalReview)), 1),
                round(float(point_4) / int(len(new_reviews) + int(totalReview)), 1),
                round(float(point_5) / int(len(new_reviews) + int(totalReview)), 1),
            ]
        return loc
    return None


def set_evaluation(location):
    pass


def get_districts():
    districts = Districts.objects.all()
    return districts


def get_cuisines():
    cuisines = Cuisines.objects.all()
    return cuisines


def get_categories():
    categories = Categories.objects.filter(pk__in=[1, 2, 3, 4, 6, 11, 12, 27,
                                                   28, 39, 43, 44, 54, 56, 79])
    return categories


def index(request):
    locations = get_locations()
    districts = get_districts()
    cuisines = get_cuisines()
    categories = get_categories()
    # for loc in locations:
    page = request.GET.get('page', 1)
    paginator = Paginator(locations, 8)
    try:
        locations = paginator.page(page)
    except PageNotAnInteger:
        locations = paginator.page(1)
    except EmptyPage:
        locations = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'locations': locations, 'districts': districts,
                                          'cuisines': cuisines, 'categories': categories})


def get_location_menu_v2(loc):
    menus = loc.menu.all().order_by('-created_at')
    return menus


def get_location_menu(loc):
    get_menu = loc.menu.all()
    menus = []

    for item in get_menu:
        menu = {}
        menu["id"] = item.id
        menu["name"] = item.name
        dishes = item.dishes
        dishes = dishes.replace("'", '"')
        dishes = dishes.replace("False", "false")
        dishes = dishes.replace("None", "null")
        try:
            menu["dishes"] = json.loads(dishes)
            for dish in menu["dishes"]:
                if 'default' in str(dish['ImageUrl']):
                    dish['ImageUrl'] = 'https://www.foody.vn/style/images/deli-dish-no-image.png'
                price = str(dish['Price']).replace('000.0', '.000')
                dish['Price'] = price
            menus.append(menu)
        except:
            return []

    return menus


def get_location_comment(loc):
    type = InteractiveTypes.objects.get(id=1)
    comments = CommentLikeShare.objects.filter(location=loc).filter(type=type).order_by('-created_at')
    return comments


def get_location_parking(loc):
    parkings = loc.parking.all()
    return parkings


def location(request, locationUrl):
    url = locationUrl
    loc = get_location_by_url(url)
    if loc:
        like_this_loc = None
        if request.user.is_authenticated:
            type = InteractiveTypes.objects.get(id=2)
            like_this_locs = CommentLikeShare.objects.filter(user=request.user).filter(location=loc).filter(type=type)
            if like_this_locs and len(like_this_locs) > 0:
                like_this_loc = like_this_locs[0]
            else:
                like_this_loc = None
        districts = get_districts()
        cuisines = get_cuisines()
        categories = get_categories()

        menuId = request.GET.get('menu', None)
        if menuId:
            # menus = loc.menu.all()
            menus = get_location_menu_v2(loc)
            if len(menus) <= 0:
                menus = None
            return render(request, 'location.html',
                          {'location': loc, 'menus': {'items': menus}, 'districts': districts,
                           'cuisines': cuisines, 'categories': categories, 'like_loc': like_this_loc})

        locate = request.GET.get('locate', None)
        price = request.GET.get('price', None)
        quality = request.GET.get('quality', None)
        serve = request.GET.get('serve', None)
        capacity = request.GET.get('serve', None)
        title = request.GET.get('title', None)
        content = request.GET.get('content', '')
        userId = request.GET.get('userId', None)

        if userId and locate and price and quality and serve and capacity and title and content:
            comment = CommentLikeShare()
            comment.user = Accounts.objects.get(id=userId)
            comment.location = loc
            comment.type = InteractiveTypes.objects.get(id=1)
            comment.title = title
            comment.content = content
            comment.evaluation = locate + ',' + price + ',' + quality + ',' + serve + ',' + capacity
            comment.score = (float(locate) + float(price) + float(quality) + float(serve) + float(capacity)) / 5
            comment.save()
            return redirect("/ha-noi/" + str(loc.url) + "/?comment=True")

        comment = request.GET.get('comment', None)
        if comment:
            comments = get_location_comment(loc)

            if len(comments) <= 0:
                comments = None
            else:
                page = request.GET.get('page', 1)

                paginator = Paginator(comments, 10)
                try:
                    comments = paginator.page(page)
                except PageNotAnInteger:
                    comments = paginator.page(1)
                except EmptyPage:
                    comments = paginator.page(paginator.num_pages)
            return render(request, 'location.html',
                          {'location': loc, 'comments': {'items': comments}, 'districts': districts,
                           'cuisines': cuisines, 'categories': categories, 'like_loc': like_this_loc})

        parking = request.GET.get('parking', None)
        if parking:
            parkings = get_location_parking(loc)
            if len(parkings) <= 0:
                parkings = None
            return render(request, 'location.html',
                          {'location': loc, 'parkings': {'items': parkings}, 'districts': districts,
                           'cuisines': cuisines, 'categories': categories, 'like_loc': like_this_loc})

        map = request.GET.get('map', None)
        if map:
            return render(request, 'location.html',
                          {'location': loc, 'map': map, 'like_loc': like_this_loc, 'districts': districts,
                           'cuisines': cuisines, 'categories': categories, })

        return render(request, 'location.html', {'location': loc, 'districts': districts,
                                                 'cuisines': cuisines, 'categories': categories,
                                                 'like_loc': like_this_loc})
    return HttpResponse('Hiện tại không có địa điểm này')


def get_suggest_location(sql1, sql2, page):
    sql = sql1 + sql2

    locations_list = Locations.objects.raw(sql)[:20]

    count = len(locations_list)

    paginator = Paginator(locations_list, 10)
    try:
        locations = paginator.page(page)
    except PageNotAnInteger:
        locations = paginator.page(1)
    except EmptyPage:
        locations = paginator.page(paginator.num_pages)
    return locations, count


def get_suggestion_location(request):
    location_id = request.GET.get('location_id', None)
    location = Locations.objects.filter(id=location_id)
    lat = None
    long = None
    if len(location) > 0:
        lat = location[0].latitude
        long = location[0].longitude
    if request.user.is_authenticated:
        userId = request.user.id
        user = Accounts.objects.get(id=userId)
        suggestion_location = user.recommend_locs
        if suggestion_location and (not suggestion_location == ''):
            if not (lat and long):
                suggestion_locations = ast.literal_eval(suggestion_location)
                suggestion_locations = sorted(suggestion_locations, key=lambda x: -x[1])
                locationId_list = [x[0] for x in suggestion_locations]
                locations_list = get_location_from_list(locationId_list)[:8]
                locations = [dict(id=m.id, name=m.name, avatar=m.avatar, url=m.url) for m in locations_list]
                locations = json.dumps(locations)
                return HttpResponse(locations, content_type='application/json', )

            else:
                suggestion_locations = ast.literal_eval(suggestion_location)
                suggestion_locations = sorted(suggestion_locations, key=lambda x: -x[1])
                locationId_list = [x[0] for x in suggestion_locations]
                id_tuple = tuple(locationId_list)
                point = f"point({long},{lat})"
                sql1 = f"select admin_locations.*,round((point(longitude,latitude) <@> {point})*1609)" \
                    f" as distance from admin_locations"
                sql2 = f" where admin_locations.is_active=TRUE and admin_locations.id in {id_tuple}" + \
                       '''order by 
                       "avgRating" desc,
                       distance asc,
                       "totalView" desc,
                       "priceMax" asc; '''

                sql = sql1 + sql2
                locations_list = Locations.objects.raw(sql)[:8]
                locations = [dict(id=m.id, name=m.name, avatar=m.avatar, url=m.url) for m in locations_list]
                locations = json.dumps(locations)
                return HttpResponse(locations, content_type='application/json', )

        if lat and long:
            point = f"point({long},{lat})"
            sql1 = f"select admin_locations.*,round((point(longitude,latitude) <@> {point})*1609)" \
                f" as distance from admin_locations"
            sql2 = ''' where admin_locations.is_active=TRUE 
                order by 

                "avgRating" desc,
                distance asc,
                "totalView" desc,

                "priceMax" asc; 
                '''

            sql = sql1 + sql2
            locations_list = Locations.objects.raw(sql)[:8]
            locations = [dict(id=m.id, name=m.name, avatar=m.avatar, url=m.url) for m in locations_list]
            locations = json.dumps(locations)
            return HttpResponse(locations, content_type='application/json', )

        else:

            sql1 = '''select admin_locations.* from admin_locations'''
            sql2 = ''' where admin_locations.is_active=TRUE 
                order by 
                "avgRating" desc,
                "totalView" desc,
                "priceMax" asc;
                '''

            sql = sql1 + sql2
            locations_list = Locations.objects.raw(sql)[:8]
            locations = [dict(id=m.id, name=m.name, avatar=m.avatar, url=m.url) for m in locations_list]
            locations = json.dumps(locations)
            return HttpResponse(locations, content_type='application/json', )

    else:
        return HttpResponse('Hãy đăng nhập để thực hiện chức năng này')


def get_location_from_list(list):
    # locations_list = []
    # for locationId in list:
    #     location = Locations.objects.get(id=locationId)
    #     locations_list.append(location)
    locations_list = Locations.objects.filter(pk__in=list).order_by('-avgRating', '-totalView', 'priceMax')
    return locations_list


def execute_word_search(word):
    word = word.replace("'", " ")
    str1 = config('str1')
    str2 = config('str2')
    word = tran_word_search(word, str1, str2)
    cursor = connection.cursor()
    word = str(word)
    sql = f"SELECT to_tsvector('{word}');"
    cursor.execute(sql)
    word = cursor.fetchall()[0][0]
    if len(word) > 0:
        word = word.split(' ')
        query = []
        for text in word:
            q = text.split(':')[0].replace("'", '')
            q += ':*'
            query.append(q)
        return query
    return None


def search(request):
    districts = get_districts()
    cuisines = get_cuisines()
    categories = get_categories()

    sort = request.GET.get('sort', None)

    word = request.GET.get('word', None)
    loc = request.GET.get('loc', None)
    cat = request.GET.get('cat', None)
    cui = request.GET.get('cui', None)
    lat = request.GET.get('lat', None)
    long = request.GET.get('long', None)
    suggest = request.GET.get('suggest', None)

    province = Provinces.objects.all()[0]
    point = f"point({province.longitude},{province.latitude})"

    page = request.GET.get('page', 1)

    # Search location
    sql1 = f"select admin_locations.*,round((point(longitude,latitude) <@> {point})*1609)" \
        f" as distance from admin_locations"
    sql2 = ' where admin_locations.is_active=TRUE'
    if not word:
        if cat:
            sql1 += ', admin_categorylocation'
            sql2 += '  and admin_locations.id=admin_categorylocation.location_id ' \
                    'and admin_categorylocation.category_id=' + cat
            'and admin_categorylocation.category_id=' + cat

        if cui:
            sql1 += ', admin_cuisinelocation'
            sql2 += ' and admin_locations.id=admin_cuisinelocation.location_id ' \
                    'and admin_cuisinelocation.cuisine_id=' + cui
        if loc:
            sql2 += ' and district_id=' + loc

        if sort == 'view':
            sql2 += ' order by "totalView" desc'
        elif sort == 'evaluate':
            sql2 += ' order by "avgRating" desc'
        elif sort == 'price':
            sql2 += ' order by "priceMax" asc'

        elif sort == 'distance':
            sql2 += ' order by "distance"  '

    if word:

        query = execute_word_search(word)
        if query:
            query = '&'.join(query)
            # query_list = []
            # for q in query.split(' '):
            #     q = q + ':*'
            #     query_list.append(q)
            # query = "&".join(query_list)

            sql1 = f"select * from (select *, ts_rank_cd(news_tsv,tsq) AS rank, " \
                f"round((point(longitude,latitude) <@> {point})*1609)" \
                f" as distance from admin_locations, to_tsquery('{query}') tsq " \
                f"where admin_locations.is_active = TRUE) S"

            # sql2 += " and news_tsv @@ to_tsquery('" + query + "')"
            sql2 = " where True"
            # where rank > 0 order by rank desc
            if cat:
                sql1 += ', admin_categorylocation'
                sql2 += ' and S.id=admin_categorylocation.location_id ' \
                        'and admin_categorylocation.category_id=' + cat
            if cui:
                sql1 += ', admin_cuisinelocation'
                sql2 += ' and S.id=admin_cuisinelocation.location_id ' \
                        'and admin_cuisinelocation.cuisine_id=' + cui
            if loc:
                sql2 += ' and district_id=' + loc

            # Sort
            sql2 += ' and rank > 0 order by rank desc'
            if sort == 'view':
                sql2 += ' ,"totalView" desc'
            elif sort == 'evaluate':
                sql2 += ' ,"avgRating" desc'
            elif sort == 'price':
                sql2 += ' ,"priceMax" asc'

            elif sort == 'distance':
                sql2 += ' ,"distance" asc '
    # else:
    #     sql2 += ' order by "totalView" desc'
    locations, count = get_search_location(sql1, sql2, page)
    return render(request, 'search.html',
                  {'locations': locations, 'districts': districts,
                   'cuisines': cuisines, 'categories': categories, 'count': count,
                   'from': "từ thành phố Hà Nội"
                   })


def get_search_location(sql1, sql2, page):
    sql = sql1 + sql2

    locations_list = Locations.objects.raw(sql)
    for location in locations_list:
        location.star = range(round(location.avgRating * 5 / 10.0))

    count = len(locations_list)

    paginator = Paginator(locations_list, 10)
    try:
        locations = paginator.page(page)
    except PageNotAnInteger:
        locations = paginator.page(1)
    except EmptyPage:
        locations = paginator.page(paginator.num_pages)
    return locations, count


def tran_word_search(word, str1, str2):
    # word = word.strip(' ')
    # word.replace("'", " ")
    # word.replace("", " ")
    # word = word.replace('  ', ' ')
    # word = word.replace(' - ', ' ')
    # word_list = []
    # for i in word.split(' '):
    #     i.strip(' ')
    #     i = "".join(list(filter(str.isalnum, i)))
    #     word_list.append(i)
    # word = " ".join(word_list)
    s = word
    # word = s
    for i in word:
        r = re.search(i, str1)
        if r:
            s = s.replace(i, str2[r.start()])
    return s


def like_create(request):
    if request.user.is_authenticated:
        locationId = request.GET.get('locationId', None)
        userId = request.GET.get('userId', None)
        if locationId and userId:
            like = CommentLikeShare()
            like.user = Accounts.objects.get(id=userId)
            location = Locations.objects.get(id=locationId)
            like.location = location
            like.type = InteractiveTypes.objects.get(id=2)
            like.save()
            location.totalFavourite += 1
            location.save()
            like_count = location.totalFavourite
            return HttpResponse(like_count)
    else:
        context = {
            'status': '400', 'reason': 'you can access this view '
        }
        response = HttpResponse(json.dumps(context), content_type='application/json')
        response.status_code = 400
        return response


def like_decreate(request):
    if request.user.is_authenticated:
        locationId = request.GET.get('locationId', None)
        userId = request.GET.get('userId', None)
        if locationId and userId:
            user = Accounts.objects.get(id=userId)
            location = Locations.objects.get(id=locationId)
            type = InteractiveTypes.objects.get(id=2)
            likes = CommentLikeShare.objects.filter(user=user).filter(location=location).filter(type=type)
            if likes and len(likes) > 0:
                likes[0].delete()
            location.totalFavourite -= 1
            location.save()
            like_count = location.totalFavourite
            return HttpResponse(like_count)
    else:
        context = {
            'status': '400', 'reason': 'you can access this view '
        }
        response = HttpResponse(json.dumps(context), content_type='application/json')
        response.status_code = 400
        return response


def view_create(request):
    if request.user.is_authenticated:
        locationId = request.GET.get('locationId', None)
        userId = request.GET.get('userId', None)
        if locationId:
            location = Locations.objects.get(id=locationId)
            location.totalView += 1
            location.save()
            if userId:
                user = Accounts.objects.get(id=userId)
                type = InteractiveTypes.objects.get(id=3)
                view = CommentLikeShare()
                view.type = type
                view.user = user
                view.location = location
                view.save()
            return HttpResponse('None')
    else:
        context = {
            'status': '400', 'reason': 'you can access this view '
        }
        response = HttpResponse(json.dumps(context), content_type='application/json')
        response.status_code = 400
        return response


def share_create(request):
    if request.user.is_authenticated:
        locationId = request.GET.get('locationId', None)
        userId = request.GET.get('userId', None)
        if locationId and userId:
            location = Locations.objects.get(id=locationId)
            user = Accounts.objects.get(id=userId)
            type = InteractiveTypes.objects.get(id=4)
            share = CommentLikeShare()
            share.type = type
            share.user = user
            share.location = location
            share.save()
        return HttpResponse('None')
    else:
        context = {
            'status': '400', 'reason': 'you can access this view '
        }
        response = HttpResponse(json.dumps(context), content_type='application/json')
        response.status_code = 400
        return response


def member(request, userId):
    if (request.user.is_authenticated and request.user.id == int(userId)) or (
            request.user.is_authenticated and request.user.id == 1):
        acc = Accounts.objects.get(id=userId)
        comment_type = InteractiveTypes.objects.get(id=1)
        comments = CommentLikeShare.objects.filter(type=comment_type).filter(user=acc).order_by('created_at')
        collections = Collections.objects.filter(user=acc).order_by('created_at')
        if len(collections) > 0:
            for coll in collections:
                if len(coll.location.all()) > 0:
                    coll.avatar = coll.location.all()[0].avatar
                else:
                    coll.avatar = "https://images.foody.vn/default/s480x300/no-image.png"
        if len(comments) <= 0:
            comments = None
        username = request.POST.get('name', None)
        if username:
            acc.name = username
            acc.save()
        if comments:
            page = request.GET.get('page', 1)
            paginator = Paginator(comments, 10)
            try:
                comments = paginator.page(page)
            except PageNotAnInteger:
                comments = paginator.page(1)
            except EmptyPage:
                comments = paginator.page(paginator.num_pages)

        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        note = request.GET.get('notification', None)
        return render(request, 'member.html',
                      {
                          'acc': acc, 'comments': comments,
                          'collections': collections, 'notifications': notifications,
                          'note': note,
                      })
    else:
        context = {
            'status': '400', 'reason': 'you can access this view '
        }
        response = HttpResponse(json.dumps(context), content_type='application/json')
        response.status_code = 400
        return response


def collection_create(request):
    if request.user.is_authenticated:
        name = request.GET.get('name', None)
        description = request.GET.get('description', None)
        userId = request.GET.get('userId', None)
        user = Accounts.objects.get(id=userId)
        collectios = []
        old_coll = Collections.objects.filter(user=user).filter(name=name)
        if len(old_coll) > 0:
            return HttpResponse('None')

        new_collection = Collections()
        new_collection.name = name
        new_collection.description = description
        new_collection.user = user
        new_collection.save()
        collectios = Collections.objects.filter(user=user).order_by('created_at')
        collectios = [dict(id=m.id, name=m.name) for m in collectios]
        return HttpResponse(
            json.dumps(collectios),
            content_type='application/json', )
    else:
        context = {
            'status': '400', 'reason': 'you can access this view '
        }
        response = HttpResponse(json.dumps(context), content_type='application/json')
        response.status_code = 400
        return response


def collection_delete(request):
    if request.user.is_authenticated:
        collection_id = request.GET.get('collectionId', None)
        if collection_id:
            Collections.objects.get(id=collection_id).delete()
            return HttpResponse('None')
    else:
        context = {
            'status': '400', 'reason': 'you can access this view '
        }
        response = HttpResponse(json.dumps(context), content_type='application/json')
        response.status_code = 400
        return response


def get_collection(request):
    if request.user.is_authenticated:
        userId = None
        if request.user.is_authenticated:
            userId = request.user.id
        user = Accounts.objects.get(id=userId)
        collections = Collections.objects.filter(user=user).order_by('created_at')
        if len(collections) > 0:
            for coll in collections:
                if len(coll.location.all()) > 0:
                    coll.avatar = coll.location.all()[0].avatar
                else:
                    coll.avatar = "https://images.foody.vn/default/s480x300/no-image.png"
        collections = [dict(id=m.id, name=m.name, avatar=m.avatar, count=len(m.location.all())) for m in collections]
        return HttpResponse(json.dumps(collections), content_type='application/json', )
    else:
        context = {
            'status': '400', 'reason': 'you can access this view '
        }
        response = HttpResponse(json.dumps(context), content_type='application/json')
        response.status_code = 400
        return response


def get_collections(request):
    if request.user.is_authenticated:
        userId = None
        if request.user.is_authenticated:
            userId = request.user.id
        user = Accounts.objects.get(id=userId)

        collections = Collections.objects.filter(user=user).order_by('created_at')

        location_id = request.GET.get('locationId', None)
        if location_id:
            location = Locations.objects.get(id=location_id)
            collections = [
                dict(id=m.id, name=m.name, count=len(m.location.all()),
                     check=len(m.location.filter(id=location_id))) for m in
                collections]
        else:
            collections = [dict(id=m.id, name=m.name, count=len(m.location.all())) for m in collections]
        return HttpResponse(json.dumps(collections), content_type='application/json', )
    else:
        context = {
            'status': '400', 'reason': 'you can access this view '
        }
        response = HttpResponse(json.dumps(context), content_type='application/json')
        response.status_code = 400
        return response


def choice_collection(request):
    if request.user.is_authenticated:
        collection_id = request.GET.get('collectionId', None)
        location_id = request.GET.get('locationId', None)
        if location_id and collection_id:
            location = Locations.objects.get(id=location_id)
            collection = Collections.objects.get(id=collection_id)
            exist = CollectionLocation.objects.filter(location=location).filter(collection=collection)
            if len(exist) > 0:
                exist[0].delete()
                return HttpResponse('delete')
            collection_location = CollectionLocation()
            collection_location.collection = collection
            collection_location.location = location
            collection_location.save()
        return HttpResponse('add')
    else:
        context = {
            'status': '400', 'reason': 'you can access this view '
        }
        response = HttpResponse(json.dumps(context), content_type='application/json')
        response.status_code = 400
        return response


def location_suggest(request):
    location_name = request.GET.get('location_name', None)

    str1 = config('str1')
    str2 = config('str2')

    sql1 = '''
       select admin_locations.* from admin_locations
      '''
    sql2 = ' where admin_locations.is_active=TRUE'

    if location_name and location_name != '':
        query = execute_word_search(location_name)
        if query:
            query = '&'.join(query)
            # query_list = []
            # for q in query.split(' '):
            #     q = q + ':*'
            #     query_list.append(q)
            # query = "&".join(query_list)

            sql2 += " and news_tsv @@ to_tsquery('" + query + "')"

        sql = sql1 + sql2
        locations_list = Locations.objects.raw(sql)[:10]
        locations = [dict(id=m.id, name=m.name, avatar=m.avatar, url=m.url) for m in locations_list]
        locations = json.dumps(locations)
        return HttpResponse(locations, content_type='application/json', )


def location_to_collection(request):
    if request.user.is_authenticated:
        locationId = request.GET.get('locationId', None)
        collectionId = request.GET.get('collectionId', None)
        location = Locations.objects.get(id=locationId)
        collection = Collections.objects.get(id=collectionId)

        ex_loc = collection.location.filter(id=locationId)
        if len(ex_loc) > 0:
            return HttpResponse('None')

        loc_collec = CollectionLocation()
        loc_collec.location = location
        loc_collec.collection = collection
        loc_collec.save()
        return HttpResponse('LocationToCollection')
    else:
        context = {
            'status': '400', 'reason': 'you can access this view '
        }
        response = HttpResponse(json.dumps(context), content_type='application/json')
        response.status_code = 400
        return response


def locations_in_collection(request):
    if request.user.is_authenticated:
        collectionId = request.GET.get('collectionId', None)
        collection = Collections.objects.get(id=collectionId)
        locations_list = collection.location.all()
        locations = [dict(id=m.id, name=m.name, avatar=m.avatar, url=m.url) for m in locations_list]
        locations = json.dumps(locations)
        return HttpResponse(locations, content_type='application/json', )
    else:
        context = {
            'status': '400', 'reason': 'you can access this view '
        }
        response = HttpResponse(json.dumps(context), content_type='application/json')
        response.status_code = 400
        return response


def delete_location_in_collection(request):
    if request.user.is_authenticated:
        collectionId = request.GET.get('collectionId', None)
        locationId = request.GET.get('locationId', None)
        collection = Collections.objects.get(id=collectionId)
        location = Locations.objects.get(id=locationId)
        CollectionLocation.objects.filter(location=location).filter(collection=collection)[0].delete()
        return HttpResponse('None')
    else:
        context = {
            'status': '400', 'reason': 'you can access this view '
        }
        response = HttpResponse(json.dumps(context), content_type='application/json')
        response.status_code = 400
        return response


def create_location(request):
    if request.user.is_authenticated:
        hourL = ["%02d" % x for x in range(24)]
        minuteL = ["%02d" % x for x in range(60)]

        categories = get_categories()
        cuisines = get_cuisines()
        services = Services.objects.all()
        districts = get_districts()

        id_max = Locations.objects.order_by('-id').first().id + 1

        nameLoc = request.GET.get('nameLoc', None)
        if request.user.is_authenticated and nameLoc:
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
            location.created_by = request.user.id

            exits_location = Locations.objects.filter(url=location.url)
            if len(exits_location) > 0:
                return HttpResponse('Tên địa điểm đã được sử dụng cho địa điểm khác')

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

            location.is_active = False
            location.save()

            service = request.GET.get('service', None)
            service_location = ServiceLocation()
            ser = Services
            if service:
                ser = ser.objects.get(id=service)
                service_location.service = ser
                service_location.location = location
                service_location.save()

            cuisine_location.save()
            category_location.save()

            userId = request.user.id
            user = Accounts.objects.get(id=userId)
            require = RequireFromUser()
            require.location = location
            require.user = user
            require.save()
            return redirect('/success')
        return render(request, 'addLocation.html', {
            'hourL': hourL, 'minuteL': minuteL,
            'cuisines': cuisines, 'services': services, 'districts': districts, 'categories': categories,
        })
    else:
        context = {
            'status': '400', 'reason': 'you can access this view '
        }
        response = HttpResponse(json.dumps(context), content_type='application/json')
        response.status_code = 400
        return response


def success(request):
    return render(request, 'success.html')


def get_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user)
        if len(notifications) > 0:
            notifications = [dict(id=m.id, count=len(notifications), content=m.content,
                                  ) for m in notifications]
            notifications = json.dumps(notifications)
            return HttpResponse(notifications, content_type='application/json', )
        else:
            context = {
                'status': '400', 'reason': 'you can access this view '
            }
            response = HttpResponse(json.dumps(context), content_type='application/json')
            response.status_code = 400
            return response
    else:
        context = {
            'status': '400', 'reason': 'you can access this view '
        }
        response = HttpResponse(json.dumps(context), content_type='application/json')
        response.status_code = 400
        return response


def get_notifications_not_view(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).filter(viewed=False)
        if len(notifications) > 0:
            notifications = [dict(id=m.id, count=len(notifications), content=m.content,
                                  userId=request.user.id) for m in notifications]
            notifications = json.dumps(notifications)
            return HttpResponse(notifications, content_type='application/json', )
        else:
            return HttpResponse(json.dumps([]), content_type='application/json', )
    else:
        context = {
            'status': '400', 'reason': 'you can access this view '
        }
        response = HttpResponse(json.dumps(context), content_type='application/json')
        response.status_code = 400
        return response


def view_notification(request):
    note_id = request.GET.get('notification', None)
    if note_id:
        note = Notification.objects.get(id=note_id)
        note.viewed = True
        note.save()
    return HttpResponse([])
