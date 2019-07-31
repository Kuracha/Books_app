# Generated by Django 2.2.2 on 2019-06-27 21:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20190627_0956'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='image',
        ),
        migrations.CreateModel(
            name='ImageLinks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('small_thumbnail', models.URLField(blank=True, default=None, verbose_name='Small thumbnail')),
                ('thumbnail', models.URLField(blank=True, default=None, verbose_name='Thumbnail')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='books.Book', verbose_name='Book')),
            ],
        ),
    ]
