import requests
from django.db import models
import datetime


class IpData(models.Model):
    ip4 = models.CharField(max_length=128, blank=True)
    ip6 = models.CharField(max_length=128, blank=True)
    userName = models.CharField(max_length=128, blank=True)
    country = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=True)
    loc = models.CharField(max_length=128, blank=True)
    org = models.CharField(max_length=128, blank=True)
    timezone = models.CharField(max_length=128, blank=True)
    hostname = models.CharField(max_length=128, blank=True)
    functionNM = models.CharField(max_length=128, blank=True)
    # brandMoser = models.CharField(max_length=128, blank=True)
    # isJsOn = models.BooleanField(blank=True)
    language = models.CharField(max_length=128, blank=True)
    date = models.CharField(max_length=128, blank=True)
    data = models.CharField(max_length=128, blank=True)

    def initIp(self, curIp):
        self.getBaseData(curIp)

    def getBaseData(self, curIp):
        endpoint = f'https://ipinfo.io/{curIp}/json'
        response = requests.get(endpoint, verify=True)

        if response.status_code != 200:
            return 'Status:', response.status_code, 'Problem with the request. Exiting.'
            exit()

        data = response.json()
        print(data)
        self.ip4 = curIp
        self.data = data
        if 'country' in data.keys():
            self.country = data['country']
        if 'city' in data.keys():
            self.city = data['city']
        if 'loc' in data.keys():
            self.loc = data['loc']
        if 'org' in data.keys():
            self.org = data['org']
        self.date = datetime.datetime.now()
        if 'timezone' in data.keys():
            self.timezone = data['timezone']
        if 'hostname' in data.keys():
            self.hostname = data['hostname']
        self.language = "ENG"

    def __str__(self):
        return f'{self.ip4} {self.userName} {self.functionNM}'


class TgUser(models.Model):
    userTgId = models.BigIntegerField(default=0)
    firstNM = models.CharField(max_length=128, blank=True)
    secondNM = models.CharField(max_length=128, blank=True)
    age = models.CharField(max_length=128, blank=True)
    rightData = models.CharField(max_length=128, blank=True)
