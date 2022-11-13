from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth import login
from .models import *
from .forms import *
from django.utils import timezone as tz
from datetime import timedelta
from django.contrib.auth.models import User
import firebase_admin
from firebase_admin import credentials, auth
from django.views.decorators.csrf import csrf_exempt
import os, json, random, string
from pprint import pprint
from django.contrib import messages

MESSAGE_TAGS = {
    messages.constants.DEBUG: 'dark',
    messages.constants.ERROR: 'danger',
}

def circle_board(request):

    context={}

    context['circle'] = get_object_or_404(Circle, pk=request.circle.id)
    context['swcs'] = Joining.objects.filter(user=request.user)\
        .exclude(circle=request.circle.id)
    context['form'] = MessageForm()
    context['cform'] = CircleForm()

    context['comments'] = Message.objects.filter(
        circle=request.circle).order_by('-posted_at')[:10]

    if(request.method == 'POST'):

        p = request.POST
        m = Message(
            circle=request.circle,
            user_posted=request.user,
            body=p['body'],
            posted_at=tz.now(),
        )
        m.save()
        messages.success(request, 'Comment is posted.')

        return redirect('app:circle_board')

    return render(request, 'circle_board.html', context)

def circle_switch(request, to_circle):

    j = Joining.objects.filter(user=request.user,circle=to_circle).first()
    if(j is None):
        raise Http404('Not be joining to this circle.')

    request.session['circle'] = to_circle

    messages.success(request, 'Switched Circle.')

    return redirect('app:circle_board')

def create_new_circle(request):

    if(request.method != 'POST'):
        return redirect('app:circle_board')

    if('name' not in request.POST):
        return redirect('app:circle_board')

    if(len(request.POST.get('name'))<1):
        messages.error(request, 'Name cannot be blank')
        return redirect('app:circle_board')

    c = Circle(name = request.POST.get('name'))
    c.save()

    j = Joining(circle = c, user = request.user)
    j.save()

    messages.success(request, 'You created Circle: '+c.name+'.')

    request.session['circle'] = c.id

    return redirect('app:circle_board')

def make_invite_url(request):

    context={}

    c = Circle.objects.filter(id=request.session['circle']).first()

    context['circle'] = c

    inv = CircleInvitation.objects.filter(circle=c,
                invited_by=request.user).first()

    if(inv is not None):
        if(inv.expired_at < tz.now()):
            inv.delete()
        else:
            context['inv'] = inv
            return render(request, 'make_invite_url.html', context)

    inv = CircleInvitation(
        circle=c,
        invited_by=request.user,
        key=''.join(random.choices(string.ascii_letters + string.digits, k=16)),
        expired_at = tz.now() + timedelta(days=7)
    )
    inv.save()
    messages.success(request, 'Invitation URL is issued.')

    context['inv'] = inv
    return render(request, 'make_invite_url.html', context)

def join_from_invite(request, key):

    inv = CircleInvitation.objects.filter(key=key).first()

    if(inv is None):
        messages.error(request, 'Ingitation key error.')
        return redirect('app:circle_board')

    j = Joining.objects.filter(
        circle = inv.circle,
        user = request.user).first()

    if( j is not None ):
        messages.error(request, 'You are already member of the invited circle.')
        pass

    else:
        j = Joining(
            circle = inv.circle,
            user = request.user
        )
        j.save()
        messages.success(request, 'Yeah! Joined to the Circle!')

    request.session['circle'] = inv.circle.id

    return redirect('app:circle_board')

def fbtest(request):
    return render(request, 'fbtest.html')

def fbtest2(request):
    return render(request, 'fbtest2.html')

def portal(request):

    if(request.user.is_authenticated):
        return redirect('app:circle_board')

    return render(request, 'portal.html')

def bridge(request):

    if(request.user.is_authenticated):
        return redirect('app:circle_board')

    return render(request, 'bridge.html')


@csrf_exempt
def tokentest(request):

    id_token = json.loads(request.body)['idtoken']
    print(id_token)

    if not firebase_admin._apps:
        cred = credentials.Certificate(
            os.path.join('/home/tky/simplecircle/simplecircle/sak.json'))
        firebase_admin.initialize_app(cred)

    decoded_token = auth.verify_id_token(id_token)
    uid = decoded_token["uid"]

    print(uid)

    print(decoded_token.items())
    print(decoded_token.values())

    return HttpResponse("MMMMM")

def trytoken(request):

    id_token = request.POST.get('token')
    if(id_token is None):
        return JsonResponse({
            'dloggedin':False,'emailvalid':False,
            'vertoken':False,'message':str(e)
        })

    # print(id_token)

    if not firebase_admin._apps:
        cred = credentials.Certificate(
            os.path.join('/home/tky/simplecircle/simplecircle/sak.json'))
        firebase_admin.initialize_app(cred)

    try:
        decoded_token = auth.verify_id_token(id_token)
    except Exception as e:
        return JsonResponse({
            'dloggedin':False,'emailvalid':False,
            'vertoken':False,'message':str(e)
        })

    print(decoded_token.items())
    print(decoded_token.values())

    uid = decoded_token["uid"]

    user = User.objects.filter(last_name=uid).first()

    if(user is not None):
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return JsonResponse({
            'dloggedin':True,'emailvalid':True,
            'error':False
        })

    if(decoded_token['firebase']['sign_in_provider'] == 'password'):
        if(decoded_token['email_verified'] == False):
            return JsonResponse({
                'dloggedin':False,'emailvalid':False,
                'vertoken':True
            })

    # Email is verified so create user
    user = User.objects.create_user(
        username = decoded_token.get('user_id'),
        email = decoded_token.get('email'),
        first_name = decoded_token['name'],
        last_name = decoded_token['uid']
    )
    user.set_unusable_password()
    user.save()

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)

    circle = Circle(
        name = 'Personal Board of ' + user.first_name
    )
    circle.save()

    j = Joining(
        user = user,
        circle = circle
    )
    j.save()

    return JsonResponse({
        'dloggedin':True,'emailvalid':True,
        'vertoken':True
    })


def register(request):

    if(request.method == 'POST'):

        if not firebase_admin._apps:
            cred = credentials.Certificate(
                os.path.join('/home/tky/simplecircle/simplecircle/sak.json'))
            firebase_admin.initialize_app(cred)

        decoded_token = auth.verify_id_token(request.POST.get('token'))

        user = User.objects.create_user(
            username = request.POST.get('name'),
            email = decoded_token['email'],
            last_name = decoded_token['uid'][0:32],
            password = "Dummy1$7@5*36("
        )
        user.save()

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

        j = Joining(
            user = user,
            circle = Circle.objects.filter(pk=4).first()
        )
        j.save()

        return redirect('app:circle_board')

    return render(request, 'register.html')

def empw_login(request):

    if(request.method != 'POST'):
        return redirect('app:portal')

    if not firebase_admin._apps:
        cred = credentials.Certificate(
            os.path.join('/home/tky/simplecircle/simplecircle/sak.json'))
        firebase_admin.initialize_app(cred)

    decoded_token = auth.verify_id_token(request.POST.get('token'))

    user = User.objects.filter(
        last_name = decoded_token['uid'][0:32]).first()
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)

    return redirect('app:circle_board')

def logout_firebase(request):
    return render(request, 'logout_firebase.html')
