# Generated migration: create Image model and add images M2M on postModel, and copy existing PostImage into Image
from django.db import migrations, models
import django.db.models.deletion


def copy_postimages_to_image(apps, schema_editor):
    PostImage = apps.get_model('blog', 'PostImage')
    Image = apps.get_model('blog', 'Image')
    Post = apps.get_model('blog', 'postModel')

    for pi in PostImage.objects.all():
        # Create or get an Image that points to the same file
        img, created = Image.objects.get_or_create(image=pi.image)
        # Link to the related post
        try:
            post = Post.objects.get(id=pi.post_id)
            post.images.add(img)
        except Post.DoesNotExist:
            continue


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_postimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='post_images')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='postmodel',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='posts', to='blog.Image'),
        ),
        migrations.RunPython(copy_postimages_to_image, migrations.RunPython.noop),
    ]
