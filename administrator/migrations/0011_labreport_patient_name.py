# Generated by Django 4.2.6 on 2023-11-01 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("administrator", "0010_rename_appoint_bill_appoint_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="labreport",
            name="patient_name",
            field=models.CharField(
                blank=True, editable=False, max_length=100, verbose_name="Patient Name"
            ),
        ),
    ]
