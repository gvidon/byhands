from django.contrib.auth.models import User
from django.core.validators     import email_re

class EmailBackend(object):
	def authenticate(self, username=None, password=None):
		try:
			user = (email_re.search(username) and User.objects.get(email=username)
				or User.objects.get(username=username))
		
		except User.DoesNotExist:
			return None
		
		if user.check_password(password):
			return user
            
	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		
		except User.DoesNotExist:
			return None
