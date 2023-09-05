from django.shortcuts import redirect

def login_successfull(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('role') == 'successfull':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')

    return wrapper

