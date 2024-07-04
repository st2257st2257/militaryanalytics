# Generated by Django 4.2.13 on 2024-07-01 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_commodity_maxduration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dronehub',
            name='specificationFile',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='abilityFlyThunderstorms',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='additionallySuppliedSoftware',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='article',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='category',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='compositionSupplyPackage',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='cruisingFlightSpeed',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='dateCommencement',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='dimensionsTransportedCargo',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='engineCapacity',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='engineType',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='extrasForModel',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='frequencyCommunication',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='link1',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='link2',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='link3',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='link4',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='link5',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='mainBranches',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='mainPurposes',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='manufacturer',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='manufacturersCountry',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='maxFlightAltitude',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='maxLengthRoute',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='maxPermissibleWindSpeed',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='minCrew',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='minQuantityToOrder',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='numberOfEngines',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='operatingTemperatureRangeAir',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='option1',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='option2',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='option3',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='overallCharacteristicsTransportCondition',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='overallCharacteristicsUAV',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='possibilityFlyingIcyConditions',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='preinstalledSoftware',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='price',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='productCompliance',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='productDescription',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='productName',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='rangeCommunicationLine',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='specification',
            field=models.TextField(blank=True, max_length=10024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='standardWarranty',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='statusReceiving',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='subCategory',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='supplierAccreditation',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='supplierLicense',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='takeoffMethod',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='typicalPayload',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='unitMeasurement',
            field=models.CharField(blank=True, max_length=2024),
        ),
        migrations.AlterField(
            model_name='dronehub',
            name='userLogin',
            field=models.CharField(blank=True, max_length=2024),
        ),
    ]