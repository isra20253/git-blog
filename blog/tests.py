from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import postModel, PostImage
from django.core.files.uploadedfile import SimpleUploadedFile
import io
from PIL import Image


def get_test_image(filename='test.png', size=(100, 100), color=(255, 0, 0)):
    f = io.BytesIO()
    Image.new('RGB', size, color).save(f, 'PNG')
    f.seek(0)
    return SimpleUploadedFile(filename, f.read(), content_type='image/png')


class ImageUploadTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='u', password='p')
        self.client.login(username='u', password='p')

    def test_upload_multiple_images(self):
        resp = self.client.post(reverse('blog-index'), {
            'title': 'T',
            'content': 'C'
        }, follow=True)
        # Now create with files
        img1 = get_test_image('one.png')
        img2 = get_test_image('two.png')
        resp = self.client.post(reverse('blog-index'), {
            'title': 'With Images',
            'content': 'C'
        }, follow=True, FILES={'images': [img1, img2]})
        post = postModel.objects.get(title='With Images')
        images = post.images.all()
        self.assertEqual(images.count(), 2)

    def test_delete_image(self):
        post = postModel.objects.create(title='P', content='C', author=self.user)
        img = PostImage.objects.create(post=post, image=get_test_image('del.png'))
        self.assertEqual(post.images.count(), 1)
        resp = self.client.post(reverse('blog-post_image_delete', args=[img.id]), follow=True)
        self.assertEqual(post.images.count(), 0)
