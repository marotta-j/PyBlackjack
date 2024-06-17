# JM
import random

suits = ['spades', 'diamonds', 'hearts', 'clubs']

ranks = ['ace', 'king', 'queen', 'jack', 10, 9, 8, 7, 6, 5, 4, 3, 2]

rank_values = {'ace': 1,
               'king': 10,
               'queen': 10,
               'jack': 10}


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return str(self.rank) + "_of_" + self.suit

    def __int__(self):
        if type(self.rank) == int:
            return self.rank
        else:
            return rank_values[self.rank]


class Deck:
    def __init__(self):
        self.cards = []

        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def draw(self):
        if len(self.cards) == 0:
            return None
        drawn = random.choice(self.cards)
        self.cards.remove(drawn)
        return drawn

    def __len__(self):
        return len(self.cards)

    def reset(self):
        self.__init__()


class BlackJackGame:
    def __init__(self):
        self.d = Deck()
        self.dealerCards = []
        self.playerCards = []
        self.standing = False
        self.pv, self.dv = 0, 0

        self.gameOver = False

    def sum(self, list):  # Give the highest possible combination
        value = 0
        aces = 0
        for card in list:
            if card.rank == "ace":
                aces += 1
            else:
                value += int(card)

        if aces > 0:
            for x in range(aces):
                value += 11
                if value > 21:
                    value -= 10

        return value

    def check_if_game_over(self):
        self.pv = self.sum(self.playerCards)
        self.dv = self.sum(self.dealerCards)

        # At anytime, if value > 21 player loses
        if self.pv > 21:
            print("Bust!")
            self.gameOver = True
            return -1

        # Beginning of the game check:
        if len(self.playerCards) == 2 and len(self.dealerCards) == 2 and self.standing is False:
            # Check if player has natural 21
            player_has_natural = False
            if self.pv == 21:
                player_has_natural = True

            # check for dealer natural blackjack
            if self.dealerCards[0].rank == "ace" or int(self.dealerCards[0]) == 10:
                if self.dv == 21:  # if the dealer has 21 natural it is either push or loss
                    self.gameOver = True
                    if player_has_natural:
                        print("Push")
                        return 0
                    else:
                        print("You lose!")
                        return -1

            if player_has_natural:  # if only you have natural blackjack you win 1.5 x bet!
                self.gameOver = True
                print('You win! Natural Blackjack!')
                return 0.5

            return None

        # End of the game check (after every stand)
        if self.dv >= 17 and self.standing:
            self.gameOver = True
            if self.dv > 21:
                print("Dealer bust!")
                return 1
            elif self.dv > self.pv:
                print("Dealer wins")
                return -1
            elif self.dv == self.pv:
                print("Push")
                return 0
            else:  # Dealer went bust
                print("You win")
                return 1

        return None

    def deal(self):  # can end in win, loss, or push
        self.d.reset()
        self.pv, self.dv = 0, 0
        self.gameOver = False
        self.standing = False
        self.dealerCards = [self.d.draw(), self.d.draw()]
        self.playerCards = [self.d.draw(), self.d.draw()]

        # Show the players cards
        print("Your cards: " + str(self.playerCards[0]) + ", " + str(self.playerCards[1]))
        print("Value = " + str(self.sum(self.playerCards)))

        print("Dealer shows: " + str(self.dealerCards[0]))

    def hit(self):
        if not self.playerCards or not self.dealerCards or self.gameOver or self.standing:
            return None
        self.playerCards.append(self.d.draw())  # Give another card
        pv = self.sum(self.playerCards)  # player value
        print("You drew: " + str(self.playerCards[-1]))
        print("Value = " + str(pv))
        return None

    def stand(self):  # this is going to stand 1 card at a time
        if not self.playerCards or not self.dealerCards or self.gameOver:
            return None

        self.standing = True

        # If we are standing for the first time, flip the dealer's other card
        if len(self.dealerCards) == 2:
            print("Dealer shows: " + str(self.dealerCards[1]) + " (Value = " + str(self.sum(self.dealerCards)) + ")")

        # Less than 17? Draw a card
        if self.sum(self.dealerCards) < 17:
            self.dealerCards.append(self.d.draw())
            print("Dealer drew: " + str(self.dealerCards[-1]) + " (Value = " + str(self.sum(self.dealerCards)) + ")")

        return None
