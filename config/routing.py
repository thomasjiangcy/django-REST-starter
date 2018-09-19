"""
Root Routing for Channels
"""

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
})
