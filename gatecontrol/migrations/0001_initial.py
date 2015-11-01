# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessRequest',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('req_time', models.DateTimeField(auto_now=True)),
                ('req_state', models.TextField(default='PENDING')),
                ('info', models.TextField()),
                ('address', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gate',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('controller_class', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='accessrequest',
            name='gate',
            field=models.ForeignKey(to='gatecontrol.Gate'),
        ),
        migrations.AddField(
            model_name='accessrequest',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
