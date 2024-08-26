# Generated by Django 4.2.2 on 2024-08-26 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("studing", "0004_course_stripe_product_id_lesson_stripe_product_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="price",
            field=models.DecimalField(
                decimal_places=2,
                default=1000,
                max_digits=10,
                verbose_name="цена курса(РУБ)",
            ),
        ),
        migrations.AddField(
            model_name="lesson",
            name="price",
            field=models.DecimalField(
                decimal_places=2,
                default=1000,
                max_digits=10,
                verbose_name="цена урока(РУБ)",
            ),
        ),
    ]
