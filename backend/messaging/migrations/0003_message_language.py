# Generated by Django 5.1.1 on 2024-12-15 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0002_message_translations'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='language',
            field=models.CharField(default='en', max_length=31, verbose_name='Content Language'),
            preserve_default=False,
        ),
    ]
