# Generated by Django 5.1.1 on 2024-12-19 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0003_message_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='Langauge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15, verbose_name='The id of the Language')),
                ('name', models.CharField(max_length=127, verbose_name='The verbose name of the Language')),
            ],
            options={
                'ordering': ('code', 'name'),
            },
        ),
    ]