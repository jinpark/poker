from django.http import HttpResponseServerError
from django.shortcuts import render_to_response
from poker.models import Game, User
from __builtin__ import None

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
        },
        context_instance=RequestContext(request)
    )

def next(request):
    """
    dealt the next card(s) for a particular game
    """
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
        },
        context_instance=RequestContext(request)
    )

FULL_DECK = [
    "d2", "d3", "d4", "d5", "d6", "d7", "d8", "d9", "dT", "dJ", "dQ", "dK", "dA",
    "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "cT", "cJ", "cQ", "cK", "cA",
    "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9", "hT", "hJ", "hQ", "hK", "hA",
    "s2", "s3", "d4", "s5", "s6", "s7", "s8", "s9", "sT", "sJ", "sQ", "sK", "sA",
]

def _random_card():
    """
    returns the random card from a FULL deck, the validity of the result will be checked in the caller
    """
    return random.choice(FULL_DECK)

def _next_cards(game):
    """
    responsible for dealing with the next card(s) depending on the stage of the game.
    special case would be the pre-flop, which would expect 3 cards to be served.
    """
    next_cards = []
    if game.stage = "pre-flop" # deal 3 cards
        for x in range(0, 3):
            # refresh the obj to make sure it's up to date
            game = Game.objects.get(guid=game.guid)
            while true:
                potential_card = _random_card()
                if potential_card not in game.community_cards and potential_card not in game.pocket_cards:
                    next_cards.append(potential_card)
                    game.community_card = game.community_card + "&potential_card"
                    game.save()
                    break;
    else:
        while True:
            potential_card = _random_card()
            if potential_card not in game.community_cards and potential_card not in game.pocket_cards:
                next_cards.append(potential_card)
                game.community_card = game.community_card + "&potential_card"
                game.save()
                break;
    return next_cards