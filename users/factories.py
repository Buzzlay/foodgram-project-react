import uuid

from django.contrib.auth import get_user_model

import factory

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for generates test User model"""
    first_name = factory.Faker('word')
    password = 'Password2?'

    class Meta:
        model = User

    @factory.lazy_attribute
    def username(self):
        return str(uuid.uuid4())

    @factory.lazy_attribute
    def email(self):
        return f'{self.username}@ya.ru'

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ''_create'' with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ''manager.create(*args, **kwargs)''
        return manager.create_user(*args, **kwargs)
