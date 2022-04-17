import datetime

from django.db import models

# Create your models here.
from users.models import User


class Product(models.Model):
    title = models.CharField(max_length=100)
    writer = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, related_name='products')
    total_amount = models.IntegerField()
    end_date = models.DateField()
    description = models.TextField()
    onetime_amount = models.IntegerField()
    now_amount = models.IntegerField()
    customers = models.ManyToManyField("users.User")

    # D-day 계산
    def d_day(self):
        now = datetime.date.today()
        tmp = list(map(int, str(self.end_date).split("-")))
        target = datetime.date(tmp[0], tmp[1], tmp[2])
        return (target - now).days

    def customer_check(self):
        return self.customers.count()

    def achievement_rate(self):
        return self.total_amount / self.now_amount

    def writer_name(self):
        return self.writer.username