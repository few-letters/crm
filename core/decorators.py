from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from .settings import LOGIN_URL

def login_required_w_message(login_url=LOGIN_URL, message="You have to be logged in."):
    
    #(Decoration Time)
    def actual_decorator(view_func):
        
        #(Run Time)
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # here we have access to all arguments above
            # message (level 1), view_func (level 2), request (level 3)
            
            if not request.user.is_authenticated:
                messages.error(request, message)
                return redirect(login_url)
            
            return view_func(request, *args, **kwargs)
            
        return _wrapped_view
    
    return actual_decorator