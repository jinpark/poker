from django.http import HttpResponseServerError
from django.shortcuts import render_to_response
from poker.models import FrenchDeck, Game, GameStages, User

def start(request):
    """
    Responsible for serving the pocket cards for the given user
    Since each user will have it's own pocket cards,
        this view requires a game guid as well as a user guid
    """
    game_guid = request.POST.get("game_guid", None)
    user_guid = request.POST.get("user_guid", None)
    if not game_guid or user_guid:
        return HttpResponseServerError()
    game = None
    user = None
    try:
        game = Game.objects.get(guid=game_guid)
        user = User.objects.get(guid=user_guid)
    except:
        return HttpResponseServerError()
    # get two pocket cards for the user
    # TODO: if re-call, return the same card
    # TODO: return in template
    return FrenchDeck.next_random_cards(2, exclude_cards=game.community_cards.append(game.pocket_cards))

def next(request):
    """
    Responsible for serving the next community card(s) for a particular game.
        depending on the current stage of the game.
    # TODO: make sure this won't be kept called,
        if re-called, same cards would be served, by fetching from game.community_cards.
    """
    game_guid = request.POST.get("game_guid", None)
    game = None
    try:
        game = Game.objects.get(guid=game_guid)
    except:
        return HttpResponseServerError()
    next_cards = FrenchDeck.next_random_cards(game.number_of_cards_needed())
    return render_to_response(
        "some_template.html",
        {
            next_cards="|".join(next_cards)
        },
        context_instance=RequestContext(request)
    )

def action(request):
    """
    Responsible for react to an action from a particular user
        from a particular game
    For example: 1. check. 2. fold. 3. call. 4. re-raise
    """
    # TODO: 1. need to update the game
    # TODO: the game need to check that all the users has entered the same state(same money or fold)
    #    before the game could be entered into the next state.
    game_guid = request.POST.get("game_guid", None)
    game = None
    try:
        game = Game.objects.get(guid=game_guid)
    except:
        return HttpResponseServerError()
    return render_to_response(
        "some_template.html",
        {
            next_cards=_next_cards(game)
            # TODO: change game stage.
        },
        context_instance=RequestContext(request)
    )

def game_status(request):
    """
    returns the current info.(cards have dealt with, bets from players etc.) of a specific game,
    from the perspective of the given user, so he can't see the pocket cards of others, of course :)
    """
    game_guid = request.GET.get("game_guid", None)
    user_guid = request.GET.get("user_guid", None)
    if not game_guid or user_guid:
        return HttpResponseServerError()
    game = None
    user = None
    try:
        game = Game.objects.get(guid=game_guid)
        user = User.objects.get(guid=user_guid)
    except:
        return HttpResponseServerError()

    pocket_cards_list = game.pocket_cards.split("|")
    pocket_cards = None
    for pocket_cards in pocket_cards_list:
        if pocket_cards.split("$")[0] == user_guid:
            pocket_cards = pocket_cards.split("$")[1]
            break
    if not pocket_cards:
        return HttpResponseServerError()
    return render_to_response(
        "some_template.html",
        {
            community_cards=game.community_cards,
            pocket_cards=pocket_cards,
            # TODO: basically return game obj :)
        },
        context_instance=RequestContext(request)
    )
