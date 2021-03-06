# Generated by Django 3.1 on 2020-11-19 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_delete_monthlysaving'),
        ('savings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberSaving',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('member', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='members.member')),
            ],
        ),
    ]
