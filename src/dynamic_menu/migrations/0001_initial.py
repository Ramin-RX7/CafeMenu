# Generated by Django 4.2.3 on 2023-08-09 02:19

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MainInfo",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=25)),
                ("motto", models.CharField(blank=True, max_length=20)),
                ("short_description", models.CharField(blank=True, max_length=150)),
                ("about_us", models.TextField(blank=True)),
                ("phone", models.CharField(max_length=15)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("logo", models.ImageField(upload_to="images/dynamic_menu/")),
                ("icon", models.ImageField(upload_to="images/dynamic_menu/")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Social",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("instagram", models.CharField(blank=True, max_length=150)),
                ("telegram", models.CharField(blank=True, max_length=150)),
                ("whatsapp", models.CharField(blank=True, max_length=150)),
                ("youtube", models.CharField(blank=True, max_length=150)),
                ("facebook", models.CharField(blank=True, max_length=150)),
                ("tweeter", models.CharField(blank=True, max_length=150)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]