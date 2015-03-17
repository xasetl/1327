from django.core.urlresolvers import reverse
from django.db import transaction
from django_webtest import WebTest
import reversion
from _1327.information_pages.models import InformationDocument

from _1327.user_management.models import UserProfile
from .models import Document


class TestRevertion(WebTest):

	csrf_checks = False

	def setUp(self):
		self.user = UserProfile.objects.create_superuser('test', 'test', 'test@test.test', 'test', 'test')
		self.user.is_active = True
		self.user.is_verified = True
		self.user.is_admin = True
		self.user.save()

		document = Document(title="title", text="text", author=self.user)
		with transaction.atomic(), reversion.create_revision():
				document.save()
				reversion.set_user(self.user)
				reversion.set_comment('test version')

		# create a second version
		document.text += '\nmore text'
		with transaction.atomic(), reversion.create_revision():
				document.save()
				reversion.set_user(self.user)
				reversion.set_comment('added more text')

	def test_only_admin_may_revert(self):
		document = Document.objects.get()
		versions = reversion.get_for_object(document)
		self.assertEqual(len(versions), 2)

		response = self.app.post(reverse('documents:revert'), {'id': versions[1].pk, 'url_title': document.url_title}, status=404)
		self.assertEqual(response.status_code, 404)

		response = self.app.post(reverse('documents:revert'), {'id': versions[1].pk, 'url_title': document.url_title}, status=403, xhr=True)
		self.assertEqual(response.status_code, 403)

		response = self.app.post(reverse('documents:revert'), {'id': versions[1].pk, 'url_title': document.url_title}, user=self.user, status=404)
		self.assertEqual(response.status_code, 404)

		response = self.app.post(reverse('documents:revert'), {'id': versions[1].pk, 'url_title': document.url_title}, user=self.user, xhr=True)
		self.assertEqual(response.status_code, 200)

	def test_revert_document(self):
		document = Document.objects.get()
		versions = reversion.get_for_object(document)
		self.assertEqual(len(versions), 2)

		# second step try to revert to old version
		response = self.app.post(reverse('documents:revert'), {'id': versions[1].pk, 'url_title': document.url_title}, user=self.user, xhr=True)
		self.assertEqual(response.status_code, 200)

		versions = reversion.get_for_object(document)
		self.assertEqual(len(versions), 3)
		self.assertEqual(versions[0].object.text, "text")
		self.assertEqual(versions[0].revision.comment, 'reverted to revision "test version"')

class TestAutosave(WebTest):

	csrf_checks = False

	def setUp(self):
		self.user = UserProfile.objects.create_superuser('test', 'test', 'test@test.test', 'test', 'test')
		self.user.is_active = True
		self.user.is_verified = True
		self.user.is_admin = True
		self.user.save()

		document = InformationDocument(title="title", text="text", author=self.user)
		with transaction.atomic(), reversion.create_revision():
				document.save()
				reversion.set_user(self.user)
				reversion.set_comment('test version')

	def test_autosave(self):
		# get document
		document = Document.objects.get()

		# document text should be text
		response = self.app.get(reverse('information_pages:edit', args=[document.url_title]), user=self.user)
		self.assertEqual(response.status_code, 200)
		form = response.form
		self.assertEqual(form.get('text').value, 'text')

		# autosave AUTO
		response = self.app.post(reverse('information_pages:autosave', args=[document.url_title]), {'text': 'AUTO', 'title': form.get('title').value, 'comment': ''}, user=self.user, xhr=True)
		self.assertEqual(response.status_code, 200)

		# if not loading autosave text should be still text
		response = self.app.get(reverse('information_pages:edit', args=[document.url_title]), user=self.user)
		self.assertEqual(response.status_code, 200)
		form = response.form
		self.assertEqual(form.get('text').value, 'text')

		# if loading autosave text should be AUTO
		response = self.app.get(reverse('information_pages:edit', args=[document.url_title]), {'restore' : ''}, user=self.user)
		self.assertEqual(response.status_code, 200)
		form = response.form
		self.assertEqual(form.get('text').value, 'AUTO')

		# second autosave AUTO2
		response = self.app.post(reverse('information_pages:autosave', args=[document.url_title]), {'text': 'AUTO2', 'title': form.get('title').value, 'comment' : ''}, user=self.user, xhr=True)
		self.assertEqual(response.status_code, 200)

		# if loading autosave text should be AUTO2
		response = self.app.get(reverse('information_pages:edit', args=[document.url_title]), {'restore' : ''}, user=self.user)
		self.assertEqual(response.status_code, 200)
		form = response.form
		self.assertEqual(form.get('text').value, 'AUTO2')
