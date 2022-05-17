from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wraper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dish:index')
        else:
            return view_func(request, *args, **kwargs)
    return wraper_func