from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_rename_postimage_related_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PostImage',
        ),
    ]
