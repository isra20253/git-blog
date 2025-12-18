from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
import io
from PIL import Image


def make_image(name, size=(600, 400), color=(255, 0, 0)):
    f = io.BytesIO()
    Image.new('RGB', size, color).save(f, 'PNG')
    f.seek(0)
    return SimpleUploadedFile(name, f.read(), content_type='image/png')


class Command(BaseCommand):
    help = 'Create a test post with multiple images via the app views (emulates a real upload)'

    def handle(self, *args, **options):
        User = get_user_model()
        user, created = User.objects.get_or_create(username='uploader')
        if created:
            user.set_password('p')
            user.email = 'uploader@example.local'
            user.save()
            self.stdout.write('Created user uploader / password p')
        else:
            self.stdout.write('User uploader already exists')

        client = Client()
        logged_in = client.login(username='uploader', password='p')
        if not logged_in:
            self.stdout.write(self.style.ERROR('Failed to log in as uploader'))
            return

        img1 = make_image('upload1.png')
        img2 = make_image('upload2.png')

        # post to the index view which handles post creation
        url = reverse('blog-index')
        # Pass HTTP_HOST to avoid DisallowedHost when using the test client
        resp = client.post(url, {'title': 'Posted via script', 'content': 'Uploaded via management command'}, files=[('images', img1), ('images', img2)], HTTP_HOST='127.0.0.1')

        # find created post
        from blog.models import postModel
        try:
            post = postModel.objects.get(title='Posted via script')
        except postModel.DoesNotExist:
            self.stdout.write(self.style.ERROR('Post not created'))
            return

        self.stdout.write(self.style.SUCCESS(f'Created post id={post.id}'))

        for img in post.images.all():
            self.stdout.write(f'Image: {img.image.url}')

        self.stdout.write('Done')
