# Generated by Django 3.1.14 on 2023-12-18 05:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classifieds', '0008_auto_20231213_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='style',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
