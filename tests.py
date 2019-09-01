from library.__init__ import app

import unittest

class TestHome(unittest.TestCase):

	def setUp(self):
		app_test = app.test_client()
		self.response = app_test.get('/')
	
	def test_get(self):
		self.assertEqual(200,self.response.status_code)

	def test_content_type(self):
		self.assertIn('text/html', self.response.content_type)

	def test_content(self):
		response_str = self.response.data.decode('utf-8')
		self.assertIn('<title>Wedding Gallery</title>', response_str)

	def test_css(self):
		response_str = self.response.data.decode('utf-8')
		self.assertIn('all.css', str(response_str))
		self.assertIn('bootstrap.min.css', str(response_str))

	def test_gallery(self):
		response_str = self.response.data.decode('utf-8')
		self.assertIn('<div class="gallery">', response_str)
		self.assertIn('sort-dropdown', response_str)
		self.assertIn('sort-gallery', response_str)
		self.assertIn('newest-to-older">', response_str)
		self.assertIn('older-to-newest">', response_str)
		self.assertIn('likes-asc">', response_str)
		self.assertIn('likes-desc">', response_str)
		self.assertIn('<div class="card-columns">', response_str)


if __name__ == '__main__':
	unittest.main()