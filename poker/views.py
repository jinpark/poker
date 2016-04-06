
def game_status(request):
    """
    returns the current info.(cards have dealt with, bets from players etc.) of a specific game.
    """
    return render_to_response(
        "some_template.html",
        {
         
        },
        context_instance=RequestContext(request)
    )
