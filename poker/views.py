from django.http import HttpResponseServerError

def game_status(request):
    """
    returns the current info.(cards have dealt with, bets from players etc.) of a specific game,
    from the perspective of the given user, so he can't see the pocket cards of others, of course :)
    """
    # assuming it's from get parameters, though we probably pass it in header. #TODO: jin :)
    game_guid = request.GET.get("game_guid", None)
    user_guid = request.GET.get("user_guid", None)
    if not game_guid or user_guid:
        return HttpResponseServerError()
    return render_to_response(
        "some_template.html",
        {
         
        },
        context_instance=RequestContext(request)
    )
