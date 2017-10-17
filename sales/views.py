from django.shortcuts import render
from accounts.models import Membership , Subscribe ,Profile
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
    print('get')
    print(request.method)
    print('post')
    print(request.POST)
    refId = request.POST.get("refId")
    resCode1 = request.POST.get('ResCode')
    saleReferenceId = request.POST.get("SaleReferenceId")
    saleOrderId = request.POST.get("SaleOrderId")
    resCode = request.POST.get("ResCode")
    print('refId :: ' + str(refId))
    print('saleReferenceId :: ' + str(saleReferenceId))
    print('saleOrderId :: ' + str(saleOrderId))
    print('resCode :: ' + str(resCode))
    print('resCode1 :: ' + str(resCode1))
    if resCode != '0':
        return render(request, 'result.html', {'token': {'success': False, 'verify_rescode': 'Incomplete Transaction'}})

    payment = Payment.objects.filter(refId=refId).first()
    payment.verify(saleReferenceId, saleOrderId)
    if payment.success:
        #what i can do in this
        a = payment.membership.subscribe.value
        p=Profile.Objects.filter(id=payment.membership.profile_id)
        import datetime
        p.expire =(datetime.date.today() + datetime.timedelta(a*365/12))
        p.save()
        return render(request, 'result.html', {'payment': payment})

