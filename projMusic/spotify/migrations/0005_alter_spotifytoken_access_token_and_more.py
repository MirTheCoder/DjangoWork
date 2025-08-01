# Generated by Django 5.2.4 on 2025-07-29 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0004_alter_spotifytoken_token_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spotifytoken',
            name='access_token',
            field=models.CharField(blank=True, default='NO_ACCESS_TOKEN_YET', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='spotifytoken',
            name='expires_in',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
