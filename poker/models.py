import uuid
import random
from django.db import models

class FrenchDeck:
    """
    represents a standard 52 card deck
        and it's related helper functions
        (mostly dealt/shuffle functions)
    """
    # https://en.wikipedia.org/wiki/Standard_52-card_deck
    # Suits:
    # d - diamond
    # c - club
    # h - heart
    # s - spade
    # Ranks:
    # 2-9 - do you really need explanation for these :)
    # T - 10
    # J - Jack
    # Q - Queen
    # K - King
    # A - Ace
    DECK_52 = [
        "d2", "d3", "d4", "d5", "d6", "d7", "d8", "d9", "dT", "dJ", "dQ", "dK", "dA",
        "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "cT", "cJ", "cQ", "cK", "cA",
        "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9", "hT", "hJ", "hQ", "hK", "hA",
        "s2", "s3", "d4", "s5", "s6", "s7", "s8", "s9", "sT", "sJ", "sQ", "sK", "sA",
    ]

    def _next_random_card(self, exclude_cards=None):
        """
        Returns a random card from a FULL or Partial DECK_52.
        NOTE: it's the caller's responsibility to:
            1. check the validity of the card(especially when exclude_cards=None).
            For example: in our texas holdem game, club of King
            would be Invalid if there is already one club of King
            served as either a pocker card or community card,
            in which case, the caller would call this method again
            until one valid card has been generated.
            2. update the exclude_cards list in some way
            For example: update the game.community_cards
            so next time this method being called, exclude_cards
            would have one more value in it.
        """
        return random.choice([x for x in self.DECK_52 if x not in exclude_cards])

    def next_random_cards(self, number_of_cards=1, exclude_cards=None):
        """
        responsible for dealing with the next number_of_cards card(s)
        """
        next_cards = []
        for x in range(0, number_of_cards):
            next_card = self._random_card(exclude_cards)
            next_cards.append(next_card)
            exclude_cards.append(next_card)
        return next_cards

class PlayerStatus:
    """play status in a game"""
    # TODO: how/when to best update these fields in a game
    Fold = "F"
    Call_Or_Check = "C" # matches the current bet
    Reraise = "R"

class GameStages:
    """stages of a game"""
    # TODO: how/when to best update these fields in a game
    Initial = "I" # no card has been dealt yet.
    PocketDone = "P" # pocket cards have been dealt
    FLopDone = "F" # flop cards have been dealt
    TurnDone = "T" # turn cards have been dealt
    RiverDone = "R" # river cards have been dealt
    GameOver = "O" # everyone looks at the winner, Jin.

class Game(models.Model):
    """
    Reprecents the CURRENT status of a poker game
    """
    STAGES = []
    guid = models.CharField(
        max_length=36, blank=True, unique=True, default=uuid.uuid4,
        help_text=(
            "Unique, externally-friendly identifier for a specific poker game"
        ),
    )
    pocket_cards = models.CharField(
        max_length=125, blank=True,
        help_text=(
            "Keeping records of the pocket cards the game have dealt with, "
            "so the next card generated from the game should never be one of them:) "
            "we will limit X=3 players at most in a game for now, "
            "so the maximum of cards will be (36+1+2*2+1)*X-1 = 125. "
            "'|' will be used as delimiter between players and "
            "'$' will be used as delimiter between player guid and his/her pocket cards."
            "for example: <guid_1>$h3h4|<guid_2>$d3d4|<guid_3>$c3c4 "
            "represents a game of 3 players each having 2 pocket cards(of course!)."
        ),
    )
    community_cards = models.CharField(
        max_length=14, blank=True,
        help_text=(
            "Keeping records of the community cards(0 ~ 5 cards) the game have dealt with "
            "using | as the delimiter. "
            "so the next card generated from the game should never be one of them:) "
            "for example: 'h3|d4|c6|s7' "
            "represents 4 cards has been dealt as community card and "
            "the current status of a game is in stage of `turn` "
        ),
    )
    players_entered = models.CharField(
        max_length=125, blank=True,
        help_text=(
            "Keeping records of the pocket cards the game have dealt with, "
            "so the next card generated from the game should never be one of them:) "
            "we will limit X=3 players at most in a game for now, "
            "so the maximum of cards will be (36+1+1+1)*X-1 = 125. "
            "'|' will be used as delimiter between players and "
            "'$' will be used as delimiter between player guid and his/her status."
            "for example: <guid_1>$h3h4|<guid_2>$d3d4|<guid_3>$c3c4 "
            "represents a game of 3 players each having 2 pocket cards(of course!)."
        ),
    )
    total_num_of_players = models.IntegerField(help_text="the total number of players who entered this game Initially.")
    stage = models.CharField(
        max_length=1,
        help_text="the current stage of the game. For exameple: F means flop has been dealt with.",
        choices=(('I', 'pre pocket cards'), ('P', "pocket"), ('F', 'flop'), ('T', 'turn'), ('R', 'river'))
    )

    bets = models.CharField(
        max_length=1000, blank=True,
        help_text=("place holder once we feel comfortable with introducing bets")
    )

    def number_of_cards_needed(self):
        """number of cards needed for the game to move into NEXT stage."""
        if self.stage == GameStages.Initial:
            return self.total_num_of_players * 2
        if self.stage == GameStages.PocketDone:
            return 3
        if self.stage in (
            GameStages.FLopDone,
            GameStages.TurnDone
        ):
            return 1
        return 0

class User(models.Model):
    """
    # Records the meta data for a user(name, chips etc) and the current game the user is in, if any.
    """
    guid = models.CharField(
        max_length=36, blank=True, unique=True, default=uuid.uuid4,
        help_text=(
            "Unique, externally-friendly identifier for a specific user"
        ),
    )
    username = models.CharField(
        max_length=20,
        help_text=(
            "Username, for example: bruce lee"
        ),
    )
