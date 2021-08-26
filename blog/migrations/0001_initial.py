# Generated by Django 3.2.5 on 2021-08-25 10:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('upload_date', models.DateTimeField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
                ('like', models.ManyToManyField(blank=True, related_name='like', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL)),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('comment_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.comment')),
                ('post_id', models.ForeignKey(db_column='post_id', default='0', on_delete=django.db.models.deletion.CASCADE, to='blog.blog')),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='writer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]