"""
Example Django integration - Add to your Django views.py
"""

from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from flow_control.login_hook import resolve_login_redirect

# Add this to your views.py

def login_view(request):
    """
    Custom login view with flow control integration.
    Add this to your Django views.py
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # INTEGRATION POINT - Single line change
            default_route = '/dashboard/'  # or settings.LOGIN_REDIRECT_URL
            redirect_url = resolve_login_redirect(str(user.id), default_route)
            
            return redirect(redirect_url)
        else:
            return render(request, 'login.html', {
                'error': 'Invalid credentials'
            })
    
    return render(request, 'login.html')


# Alternative: Override Django's LoginView
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    """
    Custom LoginView with flow control.
    Use this in your urls.py:
        path('login/', CustomLoginView.as_view(), name='login'),
    """
    def get_success_url(self):
        # Get default redirect URL
        default_route = super().get_success_url()
        
        # Apply flow control
        user_id = str(self.request.user.id)
        redirect_url = resolve_login_redirect(user_id, default_route)
        
        return redirect_url


# Example usage in urls.py:
"""
from django.urls import path
from .views import CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    # ... other routes
]
"""

