# Generated by Django 4.2.6 on 2023-10-31 05:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("administrator", "0006_rename_condition_conditions_alter_conditions_table"),
    ]

    operations = [
        migrations.RenameField(
            model_name="bill",
            old_name="appoint_id",
            new_name="appoint",
        ),
    ]
