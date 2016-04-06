from django.db import models
import uuid

class PokerGame(models.Model):
    """
    # Records the CURRENT status of a poker game
    """
    guid = models.CharField(
        max_length=36, blank=True, unique=True, default=uuid.uuid4,
        help_text=(
            "Unique, externally-friendly identifier for a specific poker game"
        ),
    )

    cards_dealt = models.CharField(
        max_length=50, blank=True,
        help_text=(
            "Keep records of the cards the game have dealt with, "
            "so the next card generated from the game will never be one of them:) "
            "we will assume there will be 10 players at most in a game. "
            "so the maximum of cards will be 10*2+5 =25. "
            "the community cards will be represented first, with "|" as the separator followed with "
            "cards dealt for each player"            
            "for example: h2dtca|<guid_1>h3h4&<guid_2>d3d4&<guid_3>c3c4 "
            "represents a game of 3 players with a flop of heart of 2, diamond of 10 and club of Ace "          
        ),
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