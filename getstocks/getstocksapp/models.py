from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=200)
    flag_img = models.CharField(max_length=200, default="BLANKFLAG.png")

    def save(self, *args, **kwargs):
        self.flag_img = f'getstocksapp/flag_images/{self.flag_img}'
        super().save(*args, **kwargs)


class Ticker(models.Model):
    ticker_name = models.CharField(max_length=200)
    full_name = models.CharField(max_length=255)
    origin_country = models.ForeignKey(Country,on_delete=models.CASCADE)
