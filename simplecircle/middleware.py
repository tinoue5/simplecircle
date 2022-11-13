from app.models import Circle, Joining
from django.shortcuts import redirect,get_object_or_404

def AppMiddleware(get_response):

    def middleware(request):

        next = request.GET.get("next")
        if(next is not None) and (not request.user.is_authenticated):
            request.session['next'] = next

        sessnext = request.session.get("next")
        if(sessnext is not None) and (request.user.is_authenticated):
            request.session['next'] = None
            return redirect(sessnext)

        if request.user.is_authenticated:
            if('circle' not in request.session):
                j = Joining.objects.filter(user=request.user).first()
                if j is None:
                    # the user is orfan!!
                    # return "error"
                    circle = None

                else:
                    # get company and set session from top hire records.
                    request.session['circle'] = j.circle.id
                    circle = j.circle

            else:
                circle = get_object_or_404(Circle, pk=request.session['circle'])

        else:
            circle = None

        request.circle = circle

        response = get_response(request)

        return response

    return middleware
