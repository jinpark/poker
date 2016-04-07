import uuid
from django.db import models

class Game(models.Model):
    """
    # Records the CURRENT status of a poker game
    """
    guid = models.CharField(
        max_length=36, blank=True, unique=True, default=uuid.uuid4,
        help_text=(
            "Unique, externally-friendly identifier for a specific poker game"
        ),
    )
    pocket_cards = models.CharField(
        max_length=40, blank=True,
        help_text=(
            "Keep records of the pocket cards the game have dealt with, "
            "so the next card generated from the game will never be one of them:) "
            "we will assume there will be 10 players at most in a game. "
            "so the maximum of cards will be 10*2 =20. "
            "'|' will be used as the separator"
            "for example: <guid_1>$h3h4|<guid_2>$d3d4|<guid_3>$c3c4 "
            "represents a game of 3 players"
        ),
    )
    community_cards = models.CharField(
        max_length=10, blank=True,
        help_text=(
            "Keep records of the community cards the game have dealt with"
            "so the next card generated from the game will never be one of them:) "
            "so the maximum of cards will be 5. "
            "for example: h3d4c6s7 "
            "represents the current status of a game in stage of `turn`"
        ),
    )

    stage = models.CharField(
        max_length=1,
        help_text="the current stage of the game. For exameple: F means flop has been dealt with.",
        choices=(('I', 'pre pocket cards'), ('P', "pocket"), ('F', 'flop'), ('T', 'turn'), ('R', 'river'))
    )

    bets = models.CharField(
        max_length=1000, blank=True,
        help_text=("place holder once we feel comfortable with introducing bets")
    )

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
