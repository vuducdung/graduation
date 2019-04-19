from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login

from app.models import Accounts
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token, account_reset_token
from django.contrib.auth import get_user_model
import json
import re

from django.core.mail import EmailMessage
from admin.models import Locations, CommentLikeShare, Districts, Cuisines, Categories, InteractiveTypes, Provinces, \
    Collections, CollectionLocation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
            user = User.objects.get(email=email)
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
            return HttpResponse("thay doi")
        else:
            return HttpResponse(request, 'reset_form.html', {'message': 'Hai mat khau khop'})
    return render(request, 'reset_form.html')


def get_locations():
    locations = Locations.objects.all().order_by('-totalView')[:12] \
        .only("id", "name", "address", "avatar", "description")
    return locations


def get_location_by_url(locationUrl):
    url = locationUrl
    loc = Locations.objects.filter(url=url).first()
    evaluation = loc.evaluation
    evaluation = evaluation.replace('[', '').replace(']', '').replace("'", "")
    # evaluation = [i.strip(' ') for i in evaluation]
    loc.evaluation = evaluation.split(',')[1:6]
    loc.evaluation = [i.strip(' ') for i in loc.evaluation]

    return loc


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

    return render(request, 'index.html', {'locations': locations, 'districts': districts,
                                          'cuisines': cuisines, 'categories': categories})


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
    comments = CommentLikeShare.objects.filter(location=loc).filter(type=type).order_by('created_at')
    return comments


def get_location_parking(loc):
    parkings = loc.parking.all()
    return parkings


def location(request, locationUrl):
    url = locationUrl
    loc = get_location_by_url(url)
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
        menus = get_location_menu(loc)
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
        comments = get_location_comment(loc).order_by('-created_at')

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
                                             'cuisines': cuisines, 'categories': categories, 'like_loc': like_this_loc})


def search(request):
    districts = get_districts()
    cuisines = get_cuisines()
    categories = get_categories()

    sort = request.GET.get('sort', None)

    word = request.GET.get('word', None)
    loc = request.GET.get('loc', None)
    cat = request.GET.get('cat', None)
    cui = request.GET.get('cui', None)
    str1 = """¹²³ÀÁẢẠÂẤẦẨẬẪÃÄÅÆàáảạâấầẩẫậãäåæĀāĂẮẰẲẴẶăắằẳẵặĄąÇçĆćĈĉĊċČčĎďĐđÈÉẸÊẾỀỄỆËèéẹêềếễệëĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨÌÍỈỊÎÏìíỉịîïĩĪīĬĭĮįİıĲĳĴĵĶķĸĹĺĻļĽľĿŀŁłÑñŃńŅņŇňŉŊŋÒÓỎỌÔỐỒỔỖỘỐỒỔỖỘƠỚỜỞỠỢÕÖòóỏọôốồổỗộơớờỡợởõöŌōŎŏŐőŒœØøŔŕŖŗŘřßŚśŜŝŞşŠšŢţŤťŦŧÙÚỦỤƯỪỨỬỮỰÛÜùúủụûưứừửữựüŨũŪūŬŭŮůŰűŲųŴŵÝýÿŶŷŸŹźŻżŽžёЁ"""
    str2 = """123AAAAAAAAAAAAAAaaaaaaaaaaaaaaAaAAAAAAaaaaaaAaCcCcCcCcCcDdDdEEEEEEEEEeeeeeeeeeEeEeEeEeEeGgGgGgGgHhHhIIIIIIIiiiiiiiIiIiIiIiIiJjKkkLlLlLlLlLlNnNnNnNnnNnOOOOOOOOOOOOOOOOOOOOOOOooooooooooooooooooOoOoOoEeOoRrRrRrSSsSsSsSsTtTtTtUUUUUUUUUUUUuuuuuuuuuuuuUuUuUuUuUuUuWwYyyYyYZzZzZzеЕ"""
    province = Provinces.objects.all()[0]
    point = 'point(' + str(province.latitude) + ',' + str(province.longitude) + ')'
    sql1 = '''
    select admin_locations.*,
   round((point(longitude,latitude) <@> point(105.85,21.033333))*1609) as distance from admin_locations
   '''
    sql2 = ' where True'

    if word:
        query = tran_word_search(word, str1, str2)
        # query = query.replace(" ", ":*&")
        query_list = []
        for q in query.split(' '):
            q = q + ':*'
            query_list.append(q)
        query = "&".join(query_list)

        sql2 += " and news_tsv @@ to_tsquery('simple','" + query + "')"

    if cat:
        sql1 += ', admin_categorylocation'
        sql2 += ' and admin_locations.id=admin_categorylocation.location_id and admin_categorylocation.category_id=' + cat
    if cui:
        sql1 += ', admin_cuisinelocation'
        sql2 += ' and admin_locations.id=admin_cuisinelocation.location_id and admin_cuisinelocation.cuisine_id=' + cui
    if loc:
        sql2 += ' and district_id=' + loc

    if sort == 'view':
        sql2 += ' order by "totalView" desc'
    if sort == 'evaluate':
        sql2 += ' order by "avgRating" desc'
    if sort == 'price':
        sql2 += ' order by "priceMax"'

    if sort == 'distance':
        sql2 += ' order by "distance"  '

    sql = sql1 + sql2
    locations = []
    locations_list = Locations.objects.raw(sql)

    count = len(locations_list)

    page = request.GET.get('page', 1)

    paginator = Paginator(locations_list, 10)
    try:
        locations = paginator.page(page)
    except PageNotAnInteger:
        locations = paginator.page(1)
    except EmptyPage:
        locations = paginator.page(paginator.num_pages)

    return render(request, 'search.html',
                  {'locations': locations, 'districts': districts,
                   'cuisines': cuisines, 'categories': categories, 'sql': sql, 'count': count})


def get_distance_location(locations, position):
    pass


def tran_word_search(word, str1, str2):
    word = word.strip(' ')
    word = word.replace(' - ', ' ')
    word_list = []
    for i in word.split(' '):
        i.strip(' ')
        i = "".join(list(filter(str.isalnum, i)))
        word_list.append(i)
    word = " ".join(word_list)
    s = word
    word = s
    for i in word:
        r = re.search(i, str1)
        if r:
            s = s.replace(i, str2[r.start()])
    return s


def like_create(request):
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


def like_decreate(request):
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


def view_create(request):
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


def share_create(request):
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


def member(request, userId):
    acc = Accounts.objects.get(id=userId)
    comment_type = InteractiveTypes.objects.get(id=1)
    comments = CommentLikeShare.objects.filter(type=comment_type).filter(user=acc)
    collections = Collections.objects.filter(user=acc).order_by('created_at')
    if len(comments) <= 0:
        comments = None
    username = request.POST.get('name', None)
    if username:
        acc.name = username
        acc.save()
    return render(request, 'member.html', {'acc': acc, 'comments': comments, 'collections': collections})


def collection_create(request):
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


def collection_delete(request):
    collection_id = request.GET.get('collectionId', None)
    if id:
        Collections.objects.get(id=collection_id).delete()


def get_collection(request):
    userId = None
    if request.user.is_authenticated:
        userId = request.user.id
    user = Accounts.objects.get(id=userId)
    collections = Collections.objects.filter(user=user).order_by('created_at')
    collections = [dict(id=m.id, name=m.name) for m in collections]
    return HttpResponse(json.dumps(collections), content_type='application/json', )


def location_suggest(request):
    location_name = request.GET.get('location_name', None)

    str1 = """¹²³ÀÁẢẠÂẤẦẨẬẪÃÄÅÆàáảạâấầẩẫậãäåæĀāĂẮẰẲẴẶăắằẳẵặĄąÇçĆćĈĉĊċČčĎďĐđÈÉẸÊẾỀỄỆËèéẹêềếễệëĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨÌÍỈỊÎÏìíỉịîïĩĪīĬĭĮįİıĲĳĴĵĶķĸĹĺĻļĽľĿŀŁłÑñŃńŅņŇňŉŊŋÒÓỎỌÔỐỒỔỖỘỐỒỔỖỘƠỚỜỞỠỢÕÖòóỏọôốồổỗộơớờỡợởõöŌōŎŏŐőŒœØøŔŕŖŗŘřßŚśŜŝŞşŠšŢţŤťŦŧÙÚỦỤƯỪỨỬỮỰÛÜùúủụûưứừửữựüŨũŪūŬŭŮůŰűŲųŴŵÝýÿŶŷŸŹźŻżŽžёЁ"""
    str2 = """123AAAAAAAAAAAAAAaaaaaaaaaaaaaaAaAAAAAAaaaaaaAaCcCcCcCcCcDdDdEEEEEEEEEeeeeeeeeeEeEeEeEeEeGgGgGgGgHhHhIIIIIIIiiiiiiiIiIiIiIiIiJjKkkLlLlLlLlLlNnNnNnNnnNnOOOOOOOOOOOOOOOOOOOOOOOooooooooooooooooooOoOoOoEeOoRrRrRrSSsSsSsSsTtTtTtUUUUUUUUUUUUuuuuuuuuuuuuUuUuUuUuUuUuWwYyyYyYZzZzZzеЕ"""

    sql1 = '''
       select admin_locations.* from admin_locations
      '''
    sql2 = ' where True'

    if location_name and location_name != '':
        query = tran_word_search(location_name, str1, str2)
        # query = query.replace(" ", ":*&")
        query_list = []
        for q in query.split(' '):
            q = q + ':*'
            query_list.append(q)
        query = "&".join(query_list)

        sql2 += " and news_tsv @@ to_tsquery('simple','" + query + "')"

        sql = sql1 + sql2
        locations_list = Locations.objects.raw(sql)[:10]
        locations = [dict(id=m.id, name=m.name, avatar=m.avatar) for m in locations_list]
        locations = json.dumps(locations)
        return HttpResponse(locations, content_type='application/json', )


def location_to_collection(request):
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
    return HttpResponse('')


def locations_in_collection(request):
    collectionId = request.GET.get('collectionId', None)
    collection = Collections.objects.get(id=collectionId)
    locations_list = collection.location.all()
    locations = [dict(id=m.id, name=m.name, avatar=m.avatar, url=m.url) for m in locations_list]
    locations = json.dumps(locations)
    return HttpResponse(locations, content_type='application/json', )


def delete_location_in_collection(request):
    collectionId = request.GET.get('collectionId', None)
    locationId = request.GET.get('locationId', None)
    collection = Collections.objects.get(id=collectionId)
    location = Locations.objects.get(id=locationId)
    CollectionLocation.objects.filter(location=location).filter(collection=collection)[0].delete()
    return HttpResponse('None')
