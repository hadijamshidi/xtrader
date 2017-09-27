from django.shortcuts import render
from accounts.models import Membership , Subscribe
from django.views.decorators.csrf import csrf_exempt
from .models import Payment
from finance.views import get_user
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


# Create your views here.
def start_pay(request, subscribe_id):

    subscribe=Subscribe.objects.get(id=subscribe_id)
    amount =subscribe.price
    mem=Membership.objects.create(subscribe=subscribe,profile=request.user.my_profile)
    payment = Payment.create(membership=mem, amount=amount)
    return render(request, "post.html", {'payment': payment})


@csrf_exempt
def payment_callback(request):
    state = request.POST.get("State")
    RefNum = request.POST.get("RefNum")
    ResNum = request.POST.get("ResNum")
    MID = request.POST.get("MID")


    if state != '0':
        from .dicerror import errorbank
        payment = Payment.objects.filter(id=ResNum).first()
        payment.success = False
        payment.failureerror = state
        return render(request, 'result.html', {'token': {'success': False, 'verify_rescode': errorbank[state]}})

    else:

        payment = Payment.objects.filter(id=ResNum).first()
        payment.verify(RefNum, MID)
        payment = Payment.objects.filter(id=ResNum).first()
        return render(request, 'result.html', {'payment': payment})
