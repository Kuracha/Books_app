# Generated by Django 2.2.2 on 2019-06-27 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='authors',
        ),
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=150, verbose_name='Authors')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to='books.Book', verbose_name='Book')),
            ],
        ),
    ]
