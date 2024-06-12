# JM
import random
import time
# TODO: Rename this file
suits = ['spades', 'diamonds', 'hearts', 'clubs']

ranks = ['ace', 'king', 'queen', 'jack', 10, 9, 8, 7, 6, 5, 4, 3, 2]

rank_values = {'ace': 1,
               'king': 10,
               'queen':10,
               'jack':10}


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

        self.gameOver = False

    def sum(self, list): # Give the highest possible combination
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

    def deal(self):
        self.d.reset()
        self.gameOver = False
        self.dealerCards = [self.d.draw(), self.d.draw()]
        self.playerCards = [self.d.draw(), self.d.draw()]

        # Show the players cards
        print("Your cards: " + str(self.playerCards[0]) + ", " + str(self.playerCards[1]))
        print("Value = " + str(self.sum(self.playerCards)))

        playerHasNatural = False
        if self.sum(self.playerCards) == 21:
            playerHasNatural = True

        # Show the dealers card and check for natural blackjack
        print("Dealer shows: " + str(self.dealerCards[0]))
        if self.dealerCards[0].rank == "ace" or int(self.dealerCards[0]) == 10:
            print("Dealer checks for natural blackjack...")
            if self.sum(self.dealerCards) == 21:  # if the dealer has 21 natural it is either push or loss
                self.gameOver = True
                if playerHasNatural:
                    print("Push")
                    return 0
                else:
                    print("You lose!")
                    return -1

        if playerHasNatural: # if only you have natural blackjack you win 1.5 x bet!
            self.gameOver = False
            print('You win! Natural Blackjack!')
            return 0.5

        return None

    def hit(self):
        self.playerCards.append(self.d.draw())
        pv = self.sum(self.playerCards)
        print("You drew: " + str(self.playerCards[-1]))
        print("Value = " + str(pv))
        if pv > 21:
            print("Bust!")
            self.gameOver = True
            return -1
        return None

    def stand(self):  # this is going to stand 1 card at a time
        if len(self.dealerCards) == 2:
            print("Dealer shows: " + str(self.dealerCards[1]) + " (Value = " + str(self.sum(self.dealerCards)) + ")")

        if self.sum(self.dealerCards) < 17:
            self.dealerCards.append(self.d.draw())
            print("Dealer drew: " + str(self.dealerCards[-1]) + " (Value = " + str(self.sum(self.dealerCards)) + ")")

        if self.sum(self.dealerCards) >= 17:
            self.gameOver = True
            if self.sum(self.dealerCards) > 21:
                print("Dealer bust!")
                return 1

            if self.sum(self.dealerCards) > self.sum(self.playerCards):
                print("Dealer wins")
                return -1
            elif self.sum(self.dealerCards) == self.sum(self.playerCards):
                print("Push")
                return 0
            else:
                print("You win") # TODO: rewrite the way return works
                return 1

        return None


    def action(self): # TODO: Depreciate this
        decision = input("(H)it or (S)tand: ")
        if decision.lower() == 'h':
            self.playerCards.append(self.d.draw())
            pv = self.sum(self.playerCards)
            print("You drew: " + str(self.playerCards[-1]))
            print("Value = " + str(pv))
            if pv > 21:
                print("Bust!")
                return -1
            return None
        elif decision.lower() != 's': # if the player said something else other than h or s
            return None
        else:
            print("Dealer shows: " + str(self.dealerCards[1]) + " (Value = " + str(self.sum(self.dealerCards)) + ")")
            time.sleep(1)

            while self.sum(self.dealerCards) < 17:
                self.dealerCards.append(self.d.draw())
                print("Dealer drew: " + str(self.dealerCards[-1]) + " (Value = " + str(self.sum(self.dealerCards)) + ")")
                time.sleep(1)


            if self.sum(self.dealerCards) > 21:
                print("Dealer bust!")
                return 1

            if self.sum(self.dealerCards) > self.sum(self.playerCards):
                print("Dealer wins")
                return -1
            elif self.sum(self.dealerCards) == self.sum(self.playerCards):
                print("Push")
                return 0
            else:
                print("You win")
                return 1

if __name__ == '__main__': # TODO: get this working again
    b = BlackJackGame()

    while True:
        if b.deal() != None:
            continue

        while True:
            if b.action() == None:
                continue
            else:
                break
