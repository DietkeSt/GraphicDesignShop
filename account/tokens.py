from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Token generator for account activation.
    """
    def _make_hash_value(self, user, timestamp):
        """
        Generates a hash value for the token.
        """
        return (
            text_type(user.pk) + text_type(timestamp) +
            text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()