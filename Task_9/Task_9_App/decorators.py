from django.shortcuts import redirect

def login_adminorfinance_successfull(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('role')=='admin' or request.session.get('role')=='finance':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')

    return wrapper


def login_adminorhr_successfull(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('role')=='admin' or request.session.get('role')=='hr':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')

    return wrapper


def login_admin_successfull(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('role')=='admin':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')

    return wrapper


def login_hr_successfull(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('role')=='hr':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')

    return wrapper


def login_finance_successfull(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get('role')=='finance':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')

    return wrapper