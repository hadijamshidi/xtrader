from django.db import models
from datetime import datetime
from pysimplesoap.client import SoapClient
from django.contrib.sites.models import Site
import traceback
from accounts.models import Profile, Membership, Subscribe
from django.db.models import Sum, Q


# Create your models here.
class Payment(models.Model):
    membership = models.ForeignKey(Membership)
    amount = models.IntegerField()
    token = models.CharField(max_length=40, null=True, blank=True)
    refNum = models.CharField(max_length=40, null=True, blank=True)
    takingDate = models.DateTimeField(default=datetime.now)
    success = models.BooleanField(default=False)
    failureerror=models.CharField(max_length=3,null=True,blank=True)

    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت ها'

    @classmethod
    def create(cls, amount, membership):
        termID = '10827265'  # کد پذیرنده     #
        payment = cls(amount=amount, membership=membership)
        payment.save()
        for i in range(1, 6):
            try:
                client = SoapClient("https://sep.shaparak.ir/Payments/InitPayment.asmx", trace=False)
                # callback = 'https://xtrader.ir/accounting/payment_callback/'
                response = client.RequestToken(TermID=termID,
                                               ResNUM=payment.id, TotalAmount=amount * 10,
                                               )
                Token = response
                payment.token = Token
                payment.save()
                return payment
            except:
                print(traceback.format_exc())

        return payment

    def verify(self, refNum, mid,):
        for i in range(1, 6):
            try:
                client = SoapClient(wsdl="https://sep.shaparak.ir/Payments/InitPayment.asmx", trace=False)
                response = client.verifyTransaction(RefNum=refNum,
                                                    MerchantID=mid,)
                self.refNum=refNum
                if self.amount == response:
                    self.success=True
                    self.save()
                else:
                    self.success=False
                    self.failureerror='تایید نکردن بانک'
                    self.save()
            except:
                print(traceback.format_exc())
