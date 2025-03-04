def menu(request):
    if request.user.is_authenticated:
        menu_start = [
            {'title': 'Main page', 'url_name': 'expenses:home'},
            {'title': 'About us', 'url_name': 'expenses:about'},
            {'title': 'Add receipt', 'url_name': 'expenses:post_receipt'},
        ]
        menu_end = [{'title': request.user.username, 'url_name': 'users:account'}]
    else:
        menu_start = [{'title': 'About us', 'url_name': 'expenses:about'}]
        menu_end = [
            {'title': 'Registration', 'url_name': 'users:register'},
            {'title': 'Login', 'url_name': 'users:login'},
        ]
    return {'menu_start': menu_start, 'menu_end': menu_end}


def active_link(request):
    return {'active_url': request.resolver_match.view_name}
