from django.shortcuts import render

from django.http import JsonResponse
from ratelimit.decorators import ratelimit

def login_view(request):
    # Apply different rate limits based on authentication status
    is_authenticated = request.user.is_authenticated
    rate = '10/m' if is_authenticated else '5/m'
    
    @ratelimit(key='ip', rate=rate, method='POST', block=True)
    def _login_view(request):
        # Simulate a login endpoint (replace with actual login logic)
        if request.method == 'POST':
            return JsonResponse({
                'status': 'success',
                'message': 'Login attempt processed',
                'user_authenticated': request.user.is_authenticated
            })
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

    return _login_view(request)