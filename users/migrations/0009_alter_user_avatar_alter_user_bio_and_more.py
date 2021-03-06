# Generated by Django 4.0a1 on 2021-10-18 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='avatars', verbose_name='avatar'),
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, verbose_name='bio'),
        ),
        migrations.AlterField(
            model_name='user',
            name='birthdate',
            field=models.DateField(blank=True, null=True, verbose_name='birthdate'),
        ),
        migrations.AlterField(
            model_name='user',
            name='currency',
            field=models.CharField(blank=True, choices=[('usd', 'USD'), ('krw', 'KRW')], default='krw', max_length=3, verbose_name='currency'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email_secret',
            field=models.CharField(blank=True, default='', max_length=20, verbose_name='email_secret'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email_verified',
            field=models.BooleanField(default=False, verbose_name='email_verified'),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], default='other', max_length=20, verbose_name='gender'),
        ),
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(blank=True, choices=[('en', 'English'), ('kr', 'Korean')], default='kr', max_length=2, verbose_name='language'),
        ),
        migrations.AlterField(
            model_name='user',
            name='login_method',
            field=models.CharField(choices=[('email', 'Email'), ('github', 'Github'), ('kakao', 'Kakao')], default='email', max_length=50, verbose_name='login_method'),
        ),
        migrations.AlterField(
            model_name='user',
            name='superhost',
            field=models.BooleanField(default=False, verbose_name='superhost'),
        ),
    ]
