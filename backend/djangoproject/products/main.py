import pandas as pd

file_errors_location = 'data.xlsx'
df = pd.read_excel(file_errors_location).head().values[0]

settings = {"userLogin": -1,
            "article": df[0],
            "manufacturer": df[1],
            "manufacturersCountry": df[2],
            "productName": df[3],
            "productType": df[4],
            "price": df[5],
            "unitMeasurement": df[6],
            "productDescription": df[7],
            "link1": df[8],
            "link2": df[9],
            "link3": df[10],
            "link4": df[11],
            "link5": df[12],
            "minQuantityToOrder": int(df[47]),
            "category": df[48]}

first = {"maxRangePayload": df[19],
         "maxTakeoffWeight": df[21],
         "maxFlightSpeed": df[24],
         "maxDuration": df[25]}

second = {"numberOfEngines": df[13],
          "engineType": df[14],
          "engineCapacity": df[15],
          "takeoffMethod": df[16],
          "rangeCommunicationLine": df[17],
          "maxFlightAltitude": df[22],
          "cruisingFlightSpeed": df[23],
          "minCrew": df[26],
          "operatingTemperatureRangeAir": df[28],
          "maxPermissibleWindSpeed": df[29],
          "overallCharacteristicsUAV": df[32],
          "typicalPayload": df[34],
          "standardWarranty": df[41],
          "mainPurposes": df[49],
          "mainBranches": df[50],
          "extrasForModel": df[51],
          "specification": df[52]}

third = {"frequencyCommunication": df[18],
         "maxLengthRoute": df[20],
         "dimensionsTransportedCargo": df[27],
         "abilityFlyThunderstorms": df[30],
         "possibilityFlyingIcyConditions": df[31],
         "overallCharacteristicsTransportCondition": df[33],
         "option1": df[35],
         "option2": df[36],
         "option3": df[37],
         "compositionSupplyPackage": df[38],
         "preinstalledSoftware": df[39],
         "additionallySuppliedSoftware": df[40],
         "dateCommencement": df[42],
         "productCompliance": df[43],
         "statusReceiving": df[44],
         "supplierLicense": df[45],
         "supplierAccreditation": df[46],
         "visibility": 1}

print(df)
for key in settings.keys():
    print(key, settings[key])

for key in first.keys():
    print(key, first[key])

for key in second.keys():
    print(key, second[key])

for key in third.keys():
    print(key, third[key])
