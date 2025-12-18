from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import postModel, PostImage, Image as ImageModel
from django.core.files.uploadedfile import SimpleUploadedFile
import io
from PIL import Image as PilImage


def get_test_image(filename='test.png', size=(100, 100), color=(255, 0, 0)):
    f = io.BytesIO()
    PilImage.new('RGB', size, color).save(f, 'PNG')
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
        # Pass multiple files for the same field as a list of tuples to the test client
        # Try sending files inside the data dict (some test client setups accept this)
        resp = self.client.post(reverse('blog-index'), {
            'title': 'With Images',
            'content': 'C',
            'images': [img1, img2]
        }, follow=True)

        post = postModel.objects.get(title='With Images')
        images = post.images.all()
        self.assertEqual(images.count(), 2)

    def test_pagination(self):
        # Create 25 posts
        for i in range(25):
            postModel.objects.create(title=f'P{i}', content='C', author=self.user)
        resp = self.client.get(reverse('blog-index'))
        self.assertEqual(resp.status_code, 200)
        # Default per_page is 10
        self.assertIn('posts', resp.context)
        self.assertEqual(len(resp.context['posts']), 10)

        resp2 = self.client.get(reverse('blog-index') + '?page=3')
        self.assertEqual(len(resp2.context['posts']), 5)

    def test_thumbnail_generation(self):
        img = ImageModel.objects.create(image=get_test_image('thumb.png'))
        # thumbnail file should exist on disk
        import os
        base, ext = os.path.splitext(img.image.path)
        thumb_path = f"{base}_thumb{ext}"
        self.assertTrue(os.path.exists(thumb_path))
        # thumbnail_url should point to the thumb
        self.assertTrue(img.thumbnail_url.endswith(f"_thumb{ext}"))

    def test_delete_image(self):
        post = postModel.objects.create(title='P', content='C', author=self.user)
        img = ImageModel.objects.create(image=get_test_image('del.png'))
        post.images.add(img)
        self.assertEqual(post.images.count(), 1)
        resp = self.client.post(reverse('blog-post_image_delete', args=[img.id]), {'post_id': post.id}, follow=True)
        post.refresh_from_db()
        self.assertEqual(post.images.count(), 0)
        # If the image has no other posts, it should be removed from disk / DB
        self.assertFalse(ImageModel.objects.filter(id=img.id).exists())
