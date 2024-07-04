# @Aleksandr Kristal v0.0.2 || add
from django.db import models
from django.contrib import admin

from users.models import User
import ast


class Status(models.Model):
    name = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)


class Product(models.Model):
    userLogin = models.CharField(max_length=1024, blank=True)
    name = models.CharField(max_length=1024)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=1024)
    type = models.CharField(max_length=1024)
    characteristicsID = models.IntegerField(default=0)
    ggz = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return f'ID: {self.id} | Владелец: {self.userLogin} | Название: {self.name}'

    def getDict(self):
        if self.type == "Commodity":
            return Commodity.objects.get(id=self.characteristicsID).getDict()
        elif self.type == "Service":
            return Service.objects.get(id=self.characteristicsID).getDict()
        elif self.type == "DroneHub":
            return DroneHub.objects.get(id=self.characteristicsID).getDict()
        else:
            return {"type": "Error"}


class SellerOrder(models.Model):
    userLogin = models.CharField(max_length=1024, blank=True)
    sellerLogin = models.CharField(max_length=1024, blank=True)
    orderIdList = models.CharField(max_length=1024, blank=True)
    productIdList = models.CharField(max_length=1024, blank=True)
    orderQuantityList = models.CharField(max_length=1024, blank=True)
    orderStatusId = models.IntegerField(default=1)

    def get_orders_id(self):
        return self.orderIdList.split(",")


    def get_orders_quantity(self):
        return self.orderIdList.split(",")


class Commodity(models.Model):
    settings = {"userLogin": "Логин пользователя",
                "article": "Артикул продукта",
                "manufacturer": "Производитель",
                "manufacturersCountry": "Страна изготовитель",
                "productName": "Название продукта",
                "subCategory": "Тип продукта",
                "price": "Цена",
                "unitMeasurement": "Единица измерения",
                "productDescription": "Описание продукта",
                "link1": "Изображение 1",
                "link2": "Изображение 2",
                "link3": "Изображение 3",
                "link4": "Изображение 4",
                "link5": "Изображение 5",
                "minQuantityToOrder": "Мин. количество для заказа",
                "category": "Категория на сайте"}
    userLogin = models.CharField(max_length=2024, blank=True)
    article = models.CharField(max_length=2024, blank=True)
    manufacturer = models.CharField(max_length=2024, blank=True)
    manufacturersCountry = models.CharField(max_length=2024, blank=True)
    productName = models.CharField(max_length=2024, blank=True)
    subCategory = models.CharField(max_length=2024, blank=True)
    price = models.CharField(max_length=2024, blank=True)
    unitMeasurement = models.CharField(max_length=2024, blank=True)
    productDescription = models.CharField(max_length=2024, blank=True)
    link1 = models.CharField(max_length=2024, blank=True)
    link2 = models.CharField(max_length=2024, blank=True)
    link3 = models.CharField(max_length=2024, blank=True)
    link4 = models.CharField(max_length=2024, blank=True)
    link5 = models.CharField(max_length=2024, blank=True)
    minQuantityToOrder = models.CharField(max_length=2024, blank=True)
    category = models.CharField(max_length=2024, blank=True)

    first = {"maxRangePayload": "Макс. дальность полёта",
             "maxTakeoffWeight": "Макс. взлетная масса",
             "maxFlightSpeed": "Макс. скорость полета",
             "maxDuration": "Макс. продолжительность полета"}
    maxRangePayload = models.CharField(max_length=2024, blank=True, default="0")
    maxTakeoffWeight = models.CharField(max_length=2024, blank=True, default="0")
    maxFlightSpeed = models.CharField(max_length=2024, blank=True, default="0")
    maxDuration = models.CharField(max_length=2024, blank=True, default="0")

    second = {"numberOfEngines": "Количество двигателей",
              "engineType": "Тип двигателя",
              "engineCapacity": "Объем двигателей",
              "takeoffMethod": "Способ запуска/взлета",
              "rangeCommunicationLine": "Дальность действия линии связи",
              "maxFlightAltitude": "Максимальная высота полета",
              "cruisingFlightSpeed": "Крейсерская скорость полета",
              "minCrew": "Минимальный состав экипажа",
              "operatingTemperatureRangeAir": "Диапазон рабочих температур воздуха",
              "maxPermissibleWindSpeed": "Максимально допустимая скорость ветра",
              "overallCharacteristicsUAV": "Габаритные характеристики БВС в рабочем состоянии",
              "typicalPayload": "Типовая полезная нагрузка в базовой версии",
              "standardWarranty": "Стандартная гарантия",
              "mainPurposes": "Основные назначения БВС",
              "mainBranches": "Основные отрасли использования БВС",
              "extrasForModel": "Все возможные допы к данной модели",
              "specification": "Спецификация",
              "specificationFile": "Файл спецификации"}
    numberOfEngines = models.CharField(max_length=2024, blank=True)
    engineType = models.CharField(max_length=2024, blank=True)
    engineCapacity = models.CharField(max_length=2024, blank=True)
    takeoffMethod = models.CharField(max_length=2024, blank=True)
    rangeCommunicationLine = models.CharField(max_length=2024, blank=True)
    maxFlightAltitude = models.CharField(max_length=2024, blank=True)
    cruisingFlightSpeed = models.CharField(max_length=2024, blank=True)
    minCrew = models.CharField(max_length=2024, blank=True)
    operatingTemperatureRangeAir = models.CharField(max_length=2024, blank=True)
    maxPermissibleWindSpeed = models.CharField(max_length=2024, blank=True)
    overallCharacteristicsUAV = models.CharField(max_length=2024, blank=True)
    typicalPayload = models.CharField(max_length=2024, blank=True)
    standardWarranty = models.CharField(max_length=2024, blank=True)
    mainPurposes = models.CharField(max_length=2024, blank=True)
    mainBranches = models.CharField(max_length=2024, blank=True)
    extrasForModel = models.CharField(max_length=2024, blank=True)
    specification = models.TextField(max_length=10024, blank=True)
    specificationFile = models.CharField(max_length=2024, blank=True)

    third = {"frequencyCommunication": "Диапазон частоты линии связи",
             "maxLengthRoute": "Максимальная длина маршрута с грузом максимальной массы",
             "dimensionsTransportedCargo": "Габариты перевозимого груза",
             "abilityFlyThunderstorms": "Возможность полетов в условиях грозы",
             "possibilityFlyingIcyConditions": "Возможность полетов в условиях обледенения",
             "overallCharacteristicsTransportCondition": "Габаритные характеристики БВС в транспортном состоянии",
             "option1": "Типовая полезная нагрузка Опция 1",
             "option2": "Типовая полезная нагрузка Опция 2",
             "option3": "Типовая полезная нагрузка Опция 3",
             "compositionSupplyPackage": "Состав комплекта поставки БАС (включая средства запуска, средства транспортировки, средства ТО",
             "preinstalledSoftware": "Предустановленное программное обеспечение с кратким описанием",
             "additionallySuppliedSoftware": "Дополнительно поставляемое программное обеспечение с кратким описанием",
             "dateCommencement": "Дата начала эксплуатации типа БВС",
             "productCompliance": "Соответствие изделия требованиям ППРФ №719 от 17.07.2015г",
             "statusReceiving": "Статус получения сертификата типа",
             "supplierLicense": "Лицензия поставщика на гостайну",
             "supplierAccreditation": "Аккредитация поставщика на ГГЗ",
             "visibility": "Видимость"}
    frequencyCommunication = models.CharField(max_length=2024, blank=True)
    maxLengthRoute = models.CharField(max_length=2024, blank=True)
    dimensionsTransportedCargo = models.CharField(max_length=2024, blank=True)
    abilityFlyThunderstorms = models.CharField(max_length=2024, blank=True)
    possibilityFlyingIcyConditions = models.CharField(max_length=2024, blank=True)
    overallCharacteristicsTransportCondition = models.CharField(max_length=2024, blank=True)
    option1 = models.CharField(max_length=2024, blank=True)
    option2 = models.CharField(max_length=2024, blank=True)
    option3 = models.CharField(max_length=2024, blank=True)
    compositionSupplyPackage = models.CharField(max_length=2024, blank=True)
    preinstalledSoftware = models.CharField(max_length=2024, blank=True)
    additionallySuppliedSoftware = models.CharField(max_length=2024, blank=True)
    dateCommencement = models.CharField(max_length=2024, blank=True)
    productCompliance = models.CharField(max_length=2024, blank=True)
    statusReceiving = models.CharField(max_length=2024, blank=True)
    supplierLicense = models.CharField(max_length=2024, blank=True)
    supplierAccreditation = models.CharField(max_length=2024, blank=True)
    visibility = models.IntegerField(default=0)

    def __str__(self):
        return f'CharacteristicsID: {self.id} | Продукт: {self.productName} | Владелец: {self.userLogin}'

    def getDictSettings(self):
        return {"userLogin": {"value": self.userLogin, "label": self.settings["userLogin"], "dimension": "text"},
                "article": {"value": self.article, "label":  self.settings["article"], "dimension": "text"},
                "manufacturer": {"value": self.manufacturer, "label":  self.settings["manufacturer"], "dimension": "text"},
                "manufacturersCountry": {"value": self.manufacturersCountry, "label":  self.settings["manufacturersCountry"], "dimension": "text"},
                "productName": {"value": self.productName, "label":  self.settings["productName"], "dimension": "text"},
                "subCategory": {"value": self.subCategory, "label":  self.settings["subCategory"], "dimension": "text"},
                "unitMeasurement": {"value": self.unitMeasurement, "label":  self.settings["unitMeasurement"], "dimension": "text"},
                "productDescription": {"value": self.productDescription, "label":  self.settings["productDescription"], "dimension": "text"},
                "link1": {"value": self.link1, "label":  self.settings["link1"], "dimension": "link"},
                "link2": {"value": self.link2, "label":  self.settings["link2"], "dimension": "link"},
                "link3": {"value": self.link3, "label":  self.settings["link3"], "dimension": "link"},
                "link4": {"value": self.link4, "label":  self.settings["link4"], "dimension": "link"},
                "link5": {"value": self.link5, "label":  self.settings["link5"], "dimension": "link"},
                "minQuantityToOrder": {"value": self.minQuantityToOrder, "label": self.settings["minQuantityToOrder"], "dimension": "шт"},
                "category": {"value": self.category, "label":  self.settings["category"], "dimension": "text"}}

    def getDictFirst(self):
        return {"maxRangePayload": {"value": self.maxRangePayload, "label": self.first["maxRangePayload"], "dimension": "км"},
                "maxTakeoffWeight": {"value": self.maxTakeoffWeight, "label": self.first["maxTakeoffWeight"], "dimension": "кг"},
                "maxFlightSpeed": {"value": self.maxFlightSpeed, "label": self.first["maxFlightSpeed"], "dimension": "км/ч"},
                "maxDuration": {"value": self.maxDuration, "label": self.first["maxDuration"], "dimension": "ч"}}

    def getDictSecond(self):
        mainPurposesDict = {"label": self.second["mainPurposes"], "dimension": "text"}
        mainPurposesStr = self.mainPurposes.split("\\")
        if self.mainPurposes[-1] == "\\":
            mainPurposesStr = self.mainPurposes.split("\\")[:-1]
        for i in range(len(mainPurposesStr)):
            item = mainPurposesStr[i]
            mainPurposesDict["value" + str(i)] = item

        mainBranchesDict = {"label": self.second["mainBranches"], "dimension": "text"}
        mainBranchesStr = self.mainBranches.split("\\")
        if self.mainBranches[-1] == "\\":
            mainBranchesStr = self.mainBranches.split("\\")[:-1]
        for i in range(len(mainBranchesStr)):
            item = mainBranchesStr[i]
            mainBranchesDict["value" + str(i)] = item

        return {"numberOfEngines": {"value": self.numberOfEngines, "label": self.second["numberOfEngines"], "dimension": "шт"},
                "engineType": {"value": self.engineType, "label": self.second["engineType"], "dimension": "text"},
                "engineCapacity": {"value": self.engineCapacity, "label": self.second["engineCapacity"], "dimension": ""},
                "takeoffMethod": {"value": self.takeoffMethod, "label": self.second["takeoffMethod"], "dimension": "text"},
                "rangeCommunicationLine": {"value": self.rangeCommunicationLine, "label": self.second["rangeCommunicationLine"], "dimension": "км"},
                "maxFlightAltitude": {"value": self.maxFlightAltitude, "label": self.second["maxFlightAltitude"], "dimension": "км"},
                "cruisingFlightSpeed": {"value": self.cruisingFlightSpeed, "label": self.second["cruisingFlightSpeed"], "dimension": "км/ч"},
                "minCrew": {"value": self.minCrew, "label": self.second["minCrew"], "dimension": "чел."},
                "operatingTemperatureRangeAir": {"value": self.operatingTemperatureRangeAir, "label": self.second["operatingTemperatureRangeAir"], "dimension": "°С"},
                "maxPermissibleWindSpeed": {"value": self.maxPermissibleWindSpeed, "label": self.second["maxPermissibleWindSpeed"], "dimension": "м/с"},
                "overallCharacteristicsUAV": {"value": self.overallCharacteristicsUAV, "label": self.second["overallCharacteristicsUAV"], "dimension": "text"},
                "typicalPayload": {"value": self.typicalPayload, "label": self.second["typicalPayload"], "dimension": "text"},
                "standardWarranty": {"value": self.standardWarranty, "label": self.second["standardWarranty"], "dimension": "text"},
                "mainPurposes": mainPurposesDict,
                "mainBranches": mainBranchesDict,
                "extrasForModel": {"value": self.extrasForModel, "label": self.second["extrasForModel"], "dimension": "text"},
                "specificationFile": {"value": self.specificationFile, "label": self.second["specificationFile"], "dimension": "text"}}

    def getDictThird(self):
        return {"frequencyCommunication": {"value": self.frequencyCommunication, "label": self.third["frequencyCommunication"], "dimension": "МГц"},
                "maxLengthRoute": {"value": self.maxLengthRoute, "label": self.third["maxLengthRoute"], "dimension": "км"},
                "dimensionsTransportedCargo": {"value": self.dimensionsTransportedCargo, "label": self.third["dimensionsTransportedCargo"], "dimension": "text"},
                "abilityFlyThunderstorms": {"value": self.abilityFlyThunderstorms, "label": self.third["abilityFlyThunderstorms"], "dimension": "text"},
                "possibilityFlyingIcyConditions": {"value": self.possibilityFlyingIcyConditions, "label": self.third["possibilityFlyingIcyConditions"], "dimension": "text"},
                "overallCharacteristicsTransportCondition": {"value": self.overallCharacteristicsTransportCondition, "label": self.third["overallCharacteristicsTransportCondition"], "dimension": "text"},
                "option1": {"value": self.option1, "label": self.third["option1"], "dimension": ""},
                "option2": {"value": self.option2, "label": self.third["option2"], "dimension": ""},
                "option3": {"value": self.option3, "label": self.third["option3"], "dimension": ""},
                "compositionSupplyPackage": {"value": self.compositionSupplyPackage, "label": self.third["compositionSupplyPackage"], "dimension": "list"},
                "preinstalledSoftware": {"value": self.preinstalledSoftware, "label": self.third["preinstalledSoftware"], "dimension": "text"},
                "additionallySuppliedSoftware": {"value": self.additionallySuppliedSoftware, "label": self.third["additionallySuppliedSoftware"], "dimension": "text"},
                "dateCommencement": {"value": self.dateCommencement, "label": self.third["dateCommencement"], "dimension": "date"},
                "productCompliance": {"value": self.productCompliance, "label": self.third["productCompliance"], "dimension": "bool"},
                "statusReceiving": {"value": self.statusReceiving, "label": self.third["statusReceiving"], "dimension": "bool"},
                "supplierLicense": {"value": self.supplierLicense, "label": self.third["supplierLicense"], "dimension": "text"},
                "supplierAccreditation": {"value": self.supplierAccreditation, "label": self.third["supplierAccreditation"], "dimension": "bool"},
                "visibility": {"value": self.visibility, "label": self.third["visibility"], "dimension": "bool"}}

    def getAllDicts(self):
        specifications = {}
        # print(self.specification,self.specification.split("\\"),len(self.specification.split("\\")))
        if len(self.specification.split("\\")) == len(self.specification.split("|")):
            for item in self.specification.split("\\"):
                # print(item,item.split("\\"),len(item.split("\\")))
                if len(item.split("|")) == 2:
                    specifications.update({item.split("|")[0]: item.split("|")[1]})
        return {"settings": self.getDictSettings(),
                "first": self.getDictFirst(),
                "second": self.getDictSecond(),
                "third": self.getDictThird(),
                "specification":
                    {"value": specifications,
                     "label": self.second["specification"]}}


class Service(models.Model):
    userLogin = models.CharField(max_length=1024, blank=True)
    article = models.CharField(max_length=1024, blank=True)
    productName = models.CharField(max_length=1024, blank=True)
    category = models.CharField(max_length=1024, blank=True)
    description = models.CharField(max_length=1024, blank=True)
    applicationScenario = models.CharField(max_length=1024, blank=True)
    subCategory = models.CharField(max_length=1024, blank=True)
    link1 = models.CharField(max_length=1024, blank=True)
    link2 = models.CharField(max_length=1024, blank=True)
    link3 = models.CharField(max_length=1024, blank=True)
    specification = models.CharField(max_length=1024, blank=True)
    visibility = models.IntegerField(default=0)
    settingsNM = {"userLogin": "Логин",
                  "article": "Артикул",
                  "productName": "Название",
                  "category": "Категория",
                  "description": "Описание",
                  "applicationScenario": "Сценарий использования",
                  "subCategory": "Подкатегория",
                  "link1": "Ссылка 1",
                  "link2": "Ссылка 2",
                  "link3": "Ссылка 3",
                  "visibility": "Видимость"}

    def __str__(self):
        return f'CharacteristicsID: {self.id} | Продукт: {self.productName} | Владелец: {self.userLogin}'

    def getDict(self):
        return {"userLogin": {"value": self.userLogin, "label": self.settingsNM["userLogin"]},
                "article": {"value": self.article, "label": self.settingsNM["article"]},
                "productName": {"value": self.productName, "label": self.settingsNM["productName"]},
                "category": {"value": self.category, "label": self.settingsNM["category"]},
                "description": {"value": self.description, "label": self.settingsNM["description"]},
                "applicationScenario": {"value": self.applicationScenario, "label": self.settingsNM["applicationScenario"]},
                "subCategory": {"value": self.subCategory, "label": self.settingsNM["subCategory"]},
                "link1": {"value": self.link1, "label": self.settingsNM["link1"]},
                "link2": {"value": self.link2, "label": self.settingsNM["link2"]},
                "link3": {"value": self.link3, "label": self.settingsNM["link3"]},
                "visibility": {"value": self.visibility, "label": self.settingsNM["visibility"]}}

    def getAllDicts(self):
        return {
            "settings": self.getDict(),
            "settingsNM": self.settingsNM
        }


class DroneHub(models.Model):
    settings = {"userLogin": "Логин пользователя",
                "article": "Артикул продукта",
                "manufacturer": "Производитель",
                "manufacturersCountry": "Страна изготовитель",
                "productName": "Название продукта",
                "subCategory": "Тип продукта",
                "price": "Цена",
                "unitMeasurement": "Единица измерения",
                "productDescription": "Описание продукта",
                "link1": "Изображение 1",
                "link2": "Изображение 2",
                "link3": "Изображение 3",
                "link4": "Изображение 4",
                "link5": "Изображение 5",
                "minQuantityToOrder": "Мин. количество для заказа",
                "category": "Категория на сайте"}
    userLogin = models.CharField(max_length=2024, blank=True)
    article = models.CharField(max_length=2024, blank=True)
    manufacturer = models.CharField(max_length=2024, blank=True)
    manufacturersCountry = models.CharField(max_length=2024, blank=True)
    productName = models.CharField(max_length=2024, blank=True)
    subCategory = models.CharField(max_length=2024, blank=True)
    price = models.CharField(max_length=2024, blank=True)
    unitMeasurement = models.CharField(max_length=2024, blank=True)
    productDescription = models.CharField(max_length=2024, blank=True)
    link1 = models.CharField(max_length=2024, blank=True)
    link2 = models.CharField(max_length=2024, blank=True)
    link3 = models.CharField(max_length=2024, blank=True)
    link4 = models.CharField(max_length=2024, blank=True)
    link5 = models.CharField(max_length=2024, blank=True)
    minQuantityToOrder = models.CharField(max_length=2024, blank=True)
    category = models.CharField(max_length=2024, blank=True)

    first = {"maxRangePayload": "Макс. дальность полёта",
             "maxTakeoffWeight": "Макс. взлетная масса",
             "maxFlightSpeed": "Макс. скорость полета",
             "maxDuration": "Макс. продолжительность полета"}
    maxRangePayload = models.CharField(max_length=2024, blank=True, default="0")
    maxTakeoffWeight = models.CharField(max_length=2024, blank=True, default="0")
    maxFlightSpeed = models.CharField(max_length=2024, blank=True, default="0")
    maxDuration = models.CharField(max_length=2024, blank=True, default="0")

    second = {"numberOfEngines": "Количество двигателей",
              "engineType": "Тип двигателя",
              "engineCapacity": "Объем двигателей",
              "takeoffMethod": "Способ запуска/взлета",
              "rangeCommunicationLine": "Дальность действия линии связи",
              "maxFlightAltitude": "Максимальная высота полета",
              "cruisingFlightSpeed": "Крейсерская скорость полета",
              "minCrew": "Минимальный состав экипажа",
              "operatingTemperatureRangeAir": "Диапазон рабочих температур воздуха",
              "maxPermissibleWindSpeed": "Максимально допустимая скорость ветра",
              "overallCharacteristicsUAV": "Габаритные характеристики БВС в рабочем состоянии",
              "typicalPayload": "Типовая полезная нагрузка в базовой версии",
              "standardWarranty": "Стандартная гарантия",
              "mainPurposes": "Основные назначения БВС",
              "mainBranches": "Основные отрасли использования БВС",
              "extrasForModel": "Все возможные допы к данной модели",
              "specification": "Спецификация",
              "specificationFile": "Файл спецификации"}
    numberOfEngines = models.CharField(max_length=2024, blank=True)
    engineType = models.CharField(max_length=2024, blank=True)
    engineCapacity = models.CharField(max_length=2024, blank=True)
    takeoffMethod = models.CharField(max_length=2024, blank=True)
    rangeCommunicationLine = models.CharField(max_length=2024, blank=True)
    maxFlightAltitude = models.CharField(max_length=2024, blank=True)
    cruisingFlightSpeed = models.CharField(max_length=2024, blank=True)
    minCrew = models.CharField(max_length=2024, blank=True)
    operatingTemperatureRangeAir = models.CharField(max_length=2024, blank=True)
    maxPermissibleWindSpeed = models.CharField(max_length=2024, blank=True)
    overallCharacteristicsUAV = models.CharField(max_length=2024, blank=True)
    typicalPayload = models.CharField(max_length=2024, blank=True)
    standardWarranty = models.CharField(max_length=2024, blank=True)
    mainPurposes = models.CharField(max_length=2024, blank=True)
    mainBranches = models.CharField(max_length=2024, blank=True)
    extrasForModel = models.CharField(max_length=2024, blank=True)
    specification = models.TextField(max_length=10024, blank=True)
    specificationFile = models.CharField(max_length=2024, blank=True)

    third = {"frequencyCommunication": "Диапазон частоты линии связи",
             "maxLengthRoute": "Максимальная длина маршрута с грузом максимальной массы",
             "dimensionsTransportedCargo": "Габариты перевозимого груза",
             "abilityFlyThunderstorms": "Возможность полетов в условиях грозы",
             "possibilityFlyingIcyConditions": "Возможность полетов в условиях обледенения",
             "overallCharacteristicsTransportCondition": "Габаритные характеристики БВС в транспортном состоянии",
             "option1": "Типовая полезная нагрузка Опция 1",
             "option2": "Типовая полезная нагрузка Опция 2",
             "option3": "Типовая полезная нагрузка Опция 3",
             "compositionSupplyPackage": "Состав комплекта поставки БАС (включая средства запуска, средства транспортировки, средства ТО",
             "preinstalledSoftware": "Предустановленное программное обеспечение с кратким описанием",
             "additionallySuppliedSoftware": "Дополнительно поставляемое программное обеспечение с кратким описанием",
             "dateCommencement": "Дата начала эксплуатации типа БВС",
             "productCompliance": "Соответствие изделия требованиям ППРФ №719 от 17.07.2015г",
             "statusReceiving": "Статус получения сертификата типа",
             "supplierLicense": "Лицензия поставщика на гостайну",
             "supplierAccreditation": "Аккредитация поставщика на ГГЗ",
             "visibility": "Видимость"}
    frequencyCommunication = models.CharField(max_length=2024, blank=True)
    maxLengthRoute = models.CharField(max_length=2024, blank=True)
    dimensionsTransportedCargo = models.CharField(max_length=2024, blank=True)
    abilityFlyThunderstorms = models.CharField(max_length=2024, blank=True)
    possibilityFlyingIcyConditions = models.CharField(max_length=2024, blank=True)
    overallCharacteristicsTransportCondition = models.CharField(max_length=2024, blank=True)
    option1 = models.CharField(max_length=2024, blank=True)
    option2 = models.CharField(max_length=2024, blank=True)
    option3 = models.CharField(max_length=2024, blank=True)
    compositionSupplyPackage = models.CharField(max_length=2024, blank=True)
    preinstalledSoftware = models.CharField(max_length=2024, blank=True)
    additionallySuppliedSoftware = models.CharField(max_length=2024, blank=True)
    dateCommencement = models.CharField(max_length=2024, blank=True)
    productCompliance = models.CharField(max_length=2024, blank=True)
    statusReceiving = models.CharField(max_length=2024, blank=True)
    supplierLicense = models.CharField(max_length=2024, blank=True)
    supplierAccreditation = models.CharField(max_length=2024, blank=True)
    visibility = models.IntegerField(default=0)

    def __str__(self):
        return f'CharacteristicsID: {self.id} | Продукт: {self.productName} | Владелец: {self.userLogin}'

    def getDictSettings(self):
        return {"userLogin": {"value": self.userLogin, "label": self.settings["userLogin"], "dimension": "text"},
                "article": {"value": self.article, "label":  self.settings["article"], "dimension": "text"},
                "manufacturer": {"value": self.manufacturer, "label":  self.settings["manufacturer"], "dimension": "text"},
                "manufacturersCountry": {"value": self.manufacturersCountry, "label":  self.settings["manufacturersCountry"], "dimension": "text"},
                "productName": {"value": self.productName, "label":  self.settings["productName"], "dimension": "text"},
                "subCategory": {"value": self.subCategory, "label":  self.settings["subCategory"], "dimension": "text"},
                "unitMeasurement": {"value": self.unitMeasurement, "label":  self.settings["unitMeasurement"], "dimension": "text"},
                "productDescription": {"value": self.productDescription, "label":  self.settings["productDescription"], "dimension": "text"},
                "link1": {"value": self.link1, "label":  self.settings["link1"], "dimension": "link"},
                "link2": {"value": self.link2, "label":  self.settings["link2"], "dimension": "link"},
                "link3": {"value": self.link3, "label":  self.settings["link3"], "dimension": "link"},
                "link4": {"value": self.link4, "label":  self.settings["link4"], "dimension": "link"},
                "link5": {"value": self.link5, "label":  self.settings["link5"], "dimension": "link"},
                "minQuantityToOrder": {"value": self.minQuantityToOrder, "label": self.settings["minQuantityToOrder"], "dimension": "шт"},
                "category": {"value": self.category, "label":  self.settings["category"], "dimension": "text"}}

    def getDictFirst(self):
        return {"maxRangePayload": {"value": self.maxRangePayload, "label": self.first["maxRangePayload"], "dimension": "км"},
                "maxTakeoffWeight": {"value": self.maxTakeoffWeight, "label": self.first["maxTakeoffWeight"], "dimension": "кг"},
                "maxFlightSpeed": {"value": self.maxFlightSpeed, "label": self.first["maxFlightSpeed"], "dimension": "км/ч"},
                "maxDuration": {"value": self.maxDuration, "label": self.first["maxDuration"], "dimension": "ч"}}

    def getDictSecond(self):
        mainPurposesDict = {"label": self.second["mainPurposes"], "dimension": "text"}
        mainPurposesStr = self.mainPurposes.split("\\")
        if self.mainPurposes[-1] == "\\":
            mainPurposesStr = self.mainPurposes.split("\\")[:-1]
        for i in range(len(mainPurposesStr)):
            item = mainPurposesStr[i]
            mainPurposesDict["value" + str(i)] = item

        mainBranchesDict = {"label": self.second["mainBranches"], "dimension": "text"}
        mainBranchesStr = self.mainBranches.split("\\")
        if self.mainBranches[-1] == "\\":
            mainBranchesStr = self.mainBranches.split("\\")[:-1]
        for i in range(len(mainBranchesStr)):
            item = mainBranchesStr[i]
            mainBranchesDict["value" + str(i)] = item

        return {"numberOfEngines": {"value": self.numberOfEngines, "label": self.second["numberOfEngines"], "dimension": "шт"},
                "engineType": {"value": self.engineType, "label": self.second["engineType"], "dimension": "text"},
                "engineCapacity": {"value": self.engineCapacity, "label": self.second["engineCapacity"], "dimension": ""},
                "takeoffMethod": {"value": self.takeoffMethod, "label": self.second["takeoffMethod"], "dimension": "text"},
                "rangeCommunicationLine": {"value": self.rangeCommunicationLine, "label": self.second["rangeCommunicationLine"], "dimension": "км"},
                "maxFlightAltitude": {"value": self.maxFlightAltitude, "label": self.second["maxFlightAltitude"], "dimension": "км"},
                "cruisingFlightSpeed": {"value": self.cruisingFlightSpeed, "label": self.second["cruisingFlightSpeed"], "dimension": "км/ч"},
                "minCrew": {"value": self.minCrew, "label": self.second["minCrew"], "dimension": "чел."},
                "operatingTemperatureRangeAir": {"value": self.operatingTemperatureRangeAir, "label": self.second["operatingTemperatureRangeAir"], "dimension": "°С"},
                "maxPermissibleWindSpeed": {"value": self.maxPermissibleWindSpeed, "label": self.second["maxPermissibleWindSpeed"], "dimension": "м/с"},
                "overallCharacteristicsUAV": {"value": self.overallCharacteristicsUAV, "label": self.second["overallCharacteristicsUAV"], "dimension": "text"},
                "typicalPayload": {"value": self.typicalPayload, "label": self.second["typicalPayload"], "dimension": "text"},
                "standardWarranty": {"value": self.standardWarranty, "label": self.second["standardWarranty"], "dimension": "text"},
                "mainPurposes": mainPurposesDict,
                "mainBranches": mainBranchesDict,
                "extrasForModel": {"value": self.extrasForModel, "label": self.second["extrasForModel"], "dimension": "text"},
                "specificationFile": {"value": self.specificationFile, "label": self.second["specificationFile"], "dimension": "text"}}

    def getDictThird(self):
        return {"frequencyCommunication": {"value": self.frequencyCommunication, "label": self.third["frequencyCommunication"], "dimension": "МГц"},
                "maxLengthRoute": {"value": self.maxLengthRoute, "label": self.third["maxLengthRoute"], "dimension": "км"},
                "dimensionsTransportedCargo": {"value": self.dimensionsTransportedCargo, "label": self.third["dimensionsTransportedCargo"], "dimension": "text"},
                "abilityFlyThunderstorms": {"value": self.abilityFlyThunderstorms, "label": self.third["abilityFlyThunderstorms"], "dimension": "text"},
                "possibilityFlyingIcyConditions": {"value": self.possibilityFlyingIcyConditions, "label": self.third["possibilityFlyingIcyConditions"], "dimension": "text"},
                "overallCharacteristicsTransportCondition": {"value": self.overallCharacteristicsTransportCondition, "label": self.third["overallCharacteristicsTransportCondition"], "dimension": "text"},
                "option1": {"value": self.option1, "label": self.third["option1"], "dimension": ""},
                "option2": {"value": self.option2, "label": self.third["option2"], "dimension": ""},
                "option3": {"value": self.option3, "label": self.third["option3"], "dimension": ""},
                "compositionSupplyPackage": {"value": self.compositionSupplyPackage, "label": self.third["compositionSupplyPackage"], "dimension": "list"},
                "preinstalledSoftware": {"value": self.preinstalledSoftware, "label": self.third["preinstalledSoftware"], "dimension": "text"},
                "additionallySuppliedSoftware": {"value": self.additionallySuppliedSoftware, "label": self.third["additionallySuppliedSoftware"], "dimension": "text"},
                "dateCommencement": {"value": self.dateCommencement, "label": self.third["dateCommencement"], "dimension": "date"},
                "productCompliance": {"value": self.productCompliance, "label": self.third["productCompliance"], "dimension": "bool"},
                "statusReceiving": {"value": self.statusReceiving, "label": self.third["statusReceiving"], "dimension": "bool"},
                "supplierLicense": {"value": self.supplierLicense, "label": self.third["supplierLicense"], "dimension": "text"},
                "supplierAccreditation": {"value": self.supplierAccreditation, "label": self.third["supplierAccreditation"], "dimension": "bool"},
                "visibility": {"value": self.visibility, "label": self.third["visibility"], "dimension": "bool"}}

    def getAllDicts(self):
        specifications = {}
        # print(self.specification,self.specification.split("\\"),len(self.specification.split("\\")))
        if len(self.specification.split("\\")) == len(self.specification.split("|")):
            for item in self.specification.split("\\"):
                # print(item,item.split("\\"),len(item.split("\\")))
                if len(item.split("|")) == 2:
                    specifications.update({item.split("|")[0]: item.split("|")[1]})
        return {"settings": self.getDictSettings(),
                "first": self.getDictFirst(),
                "second": self.getDictSecond(),
                "third": self.getDictThird(),
                "specification":
                    {"value": specifications,
                     "label": self.second["specification"]}}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ("id", "userLogin", "name", )
    list_display = ("id", "userLogin", "name")


@admin.register(Commodity)
class CommodityAdmin(admin.ModelAdmin):
    search_fields = ("id", "userLogin", "productName", )
    list_display = ("id", "userLogin", "productName")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    search_fields = ("id", "userLogin", "productName", )
    list_display = ("id", "userLogin", "productName")


@admin.register(DroneHub)
class DroneHubAdmin(admin.ModelAdmin):
    search_fields = ("id", "userLogin", "productName", )
    list_display = ("id", "userLogin", "productName")


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "description", )
    list_display = ("id", "name", "description")


@admin.register(SellerOrder)
class SellerOrderAdmin(admin.ModelAdmin):
    search_fields = ("id", "userLogin", "sellerLogin",)
    list_display = ("id", "userLogin", "sellerLogin")


class ListField(models.TextField):
    pass
