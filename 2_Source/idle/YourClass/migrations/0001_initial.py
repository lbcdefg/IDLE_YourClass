# Generated by Django 4.1.6 on 2023-02-28 17:08

import ckeditor_uploader.fields
import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Categories",
            fields=[
                (
                    "Cat_name",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
                ("Cat_info", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="ClassNames",
            fields=[
                (
                    "classnames",
                    models.CharField(max_length=30, primary_key=True, serialize=False),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Member",
            fields=[
                ("email", models.TextField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=30)),
                ("password", models.CharField(max_length=30)),
                (
                    "rdate",
                    models.DateTimeField(
                        default=datetime.datetime(2023, 2, 28, 17, 8, 9, 958784)
                    ),
                ),
                ("dept", models.CharField(max_length=10)),
                ("fire", models.CharField(max_length=2)),
                (
                    "classnames",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="YourClass.classnames",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                (
                    "date",
                    models.DateTimeField(
                        default=datetime.datetime(2023, 2, 28, 17, 8, 9, 958784)
                    ),
                ),
                ("body", ckeditor_uploader.fields.RichTextUploadingField()),
                ("file", models.TextField(null=True)),
                ("viewcount", models.PositiveIntegerField(default=0)),
                ("post_fix", models.BooleanField(default=False)),
                ("post_like", models.PositiveIntegerField(default=0)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="YourClass.member",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="YourClass.categories",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Like",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "like_post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="YourClass.post"
                    ),
                ),
                (
                    "like_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="YourClass.member",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "comment_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("comment_text", models.TextField()),
                (
                    "comment_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="YourClass.member",
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="YourClass.post",
                    ),
                ),
            ],
        ),
    ]
