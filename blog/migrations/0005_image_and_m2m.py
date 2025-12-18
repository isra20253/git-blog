# Generated migration: create Image model and add images M2M on postModel, and copy existing PostImage into Image
from django.db import migrations, models
import django.db.models.deletion


def copy_postimages_to_image(apps, schema_editor):
    PostImage = apps.get_model('blog', 'PostImage')
    Image = apps.get_model('blog', 'Image')
    Post = apps.get_model('blog', 'postModel')

    through = Post._meta.get_field('images').remote_field.through

    for pi in PostImage.objects.all():
        # Create or get an Image that points to the same file
        img, created = Image.objects.get_or_create(image=pi.image)
        # Link to the related post, handling different through models
        try:
            post = Post.objects.get(id=pi.post_id)
        except Post.DoesNotExist:
            continue

        # If the M2M uses an auto-created through model (normal), insert a through instance linking post<->image
        if getattr(through._meta, 'auto_created', False):
            # find field names for the relations to post and image
            fk_to_post = None
            fk_to_image = None
            for f in through._meta.fields:
                if getattr(f, 'is_relation', False) and getattr(f, 'related_model', None) is Post:
                    fk_to_post = f.name
                if getattr(f, 'is_relation', False) and getattr(f, 'related_model', None) is Image:
                    fk_to_image = f.name
            kwargs = {}
            if fk_to_post:
                kwargs[fk_to_post] = post
            if fk_to_image:
                kwargs[fk_to_image] = img
            through.objects.create(**kwargs)
        else:
            # Legacy through model (likely PostImage) – create a legacy instance referencing the same file
            try:
                through.objects.create(post=post, image=pi.image)
            except Exception:
                # best effort: skip if schema mismatch
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
