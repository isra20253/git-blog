from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_image_and_m2m'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimage',
            name='post',
            field=models.ForeignKey(related_name='legacy_images', on_delete=models.CASCADE, to='blog.postmodel'),
        ),
    ]
