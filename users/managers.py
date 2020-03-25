from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, first_name, last_name, password="password", **kwargs):
        if not email:
            raise ValueError('Employees must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name,
                        last_name=last_name, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user