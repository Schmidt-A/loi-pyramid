from pyramid.view import notfound_view_config


# TODO: do we want to keep these to pass relevant data to HTTP errs?
@notfound_view_config(renderer='json')
def notfound_view(request):
    request.response.status = 404
    return {}
