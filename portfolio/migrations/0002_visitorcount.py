from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('portfolio', '0001_initial'),
    ]
    operations = [
        migrations.CreateModel(
            name='VisitorCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, unique=True)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
    ]