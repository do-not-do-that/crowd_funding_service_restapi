import datetime

from django.db import models

# Create your models here.
from users.models import User


class Product(models.Model):
    title = models.CharField(max_length=100)
    writer = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name='products')
    total_amount = models.IntegerField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)
    description = models.TextField()
    onetime_amount = models.IntegerField(blank=False, null=False)
    now_amount = models.IntegerField(default=0)
    customers = models.ManyToManyField("users.User")
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    # D-day 계산
    def d_day(self):
        now = datetime.date.today()
        tmp = list(map(int, str(self.end_date).split("-")))
        target = datetime.date(tmp[0], tmp[1], tmp[2])
        return (target - now).days

    def customer_check(self):
        return self.customers.count()

    def achievement_rate(self):
        return f'{(self.now_amount / self.total_amount) *100 :.0f}%'
