from django.shortcuts import redirect

def login_admin_successfull(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('role')=='admin':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')

    return wrapper