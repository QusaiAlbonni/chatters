from typing import Callable
from urllib.parse import parse_qs
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser, AnonymousUser
from channels.db import database_sync_to_async


async def get_user_by_token(token: str) -> AbstractUser:
    """
    Asynchronously retrieve a user by their authentication token.
    
    Args:
        token (str): The authentication token to validate
        
    Returns:
        AbstractUser: The authenticated user or AnonymousUser if token is invalid
    """
    try:
        return (await Token.objects.select_related('user').aget(key=token)).user
    except Token.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware:
    """
    Custom middleware for token-based authentication in Django Channels.
    
    Extracts token from query parameters and authenticates the user.
    Falls back to AnonymousUser if no token is provided or token is invalid.
    """
    
    def __init__(self, inner: Callable):
        self.inner = inner
    
    async def __call__(self, scope, receive, send):
        # Create a mutable copy of the scope
        scope = dict(scope)
        
        try:
            # Get query parameters
            query_string = scope.get("query_string", b"").decode()
            query_dict = parse_qs(query_string)
            
            # Extract token from query parameters
            token = query_dict.get("token", [None])[0]
            
            if token:
                # Authenticate user with token
                user = await get_user_by_token(token)
            else:
                user = AnonymousUser()
                
        except Exception as e:
            # Fall back to AnonymousUser on any error
            user = AnonymousUser()
        
        # Add user to scope
        scope["user"] = user
        
        # Call the inner application
        return await self.inner(scope, receive, send)