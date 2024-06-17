import pygame
import os
import game_engine

# Initialize Pygame
pygame.init()

# Fonts
font = pygame.font.Font('freesansbold.ttf', 40)  # Normal Font
small_font = pygame.font.Font('freesansbold.ttf', 20)  # Smaller Font

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 128, 0)  # Green background
CARD_WIDTH, CARD_HEIGHT = 91, 116  # Typical card dimensions
CARD_GAP = 20  # Space between cards

# Paths
CARD_IMAGES_PATH = "cards"

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack Dealer's Table")


# Load card images
def load_card_image(card_name):
    card_image = pygame.image.load(os.path.join(CARD_IMAGES_PATH, f"{card_name}.png"))
    return pygame.transform.scale(card_image, (CARD_WIDTH, CARD_HEIGHT))


# Function to display a hand of cards
def display_hand(hand, start_x, start_y):
    for i, card in enumerate(hand):
        card_image = load_card_image(card)
        screen.blit(card_image, (start_x + i * (CARD_WIDTH + CARD_GAP), start_y))


def show_game_over(status):
    if status == 0:
        screen.blit(font.render("Push", True, (0, 0, 0)), (30, 540))
    elif status == 1:
        screen.blit(font.render("You win!", True, (0, 0, 0)), (30, 540))
    else:
        screen.blit(font.render("You lose :(", True, (0, 0, 0)), (30, 540))


# Setup game engine
b = game_engine.BlackJackGame()
b.deal()
playerCards = b.playerCards
dealerCards = [b.dealerCards[0], "back"]


standing = False
running = True
while running:
    screen.fill(BACKGROUND_COLOR)

    # First check if the game is over
    status = b.check_if_game_over()
    if status is not None:
        show_game_over(status)
        dealerCards = b.dealerCards
        standing = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == "return":
                b.hit()
            elif pygame.key.name(event.key) == "space":
                standing = True
                dealerCards = b.dealerCards

    # Display player's hand
    player_start_x = (SCREEN_WIDTH - (len(playerCards) * (CARD_WIDTH + CARD_GAP) - CARD_GAP)) // 2
    display_hand(playerCards, player_start_x, 400)

    # Display player's hand value
    screen.blit(font.render(str(b.pv), True, (255, 255, 255)), (350, 540))

    # Display dealer's hand value
    if standing:
        screen.blit(font.render(str(b.dv), True, (255, 255, 255)), (350, 225))

    # Display dealer's hand
    dealer_start_x = (SCREEN_WIDTH - (len(dealerCards) * (CARD_WIDTH + CARD_GAP) - CARD_GAP)) // 2
    display_hand(dealerCards, dealer_start_x, 100)

    # Update the display
    pygame.display.update()

    if b.gameOver:
        pygame.time.wait(4000)
        b.deal()
        playerCards = b.playerCards
        dealerCards = [b.dealerCards[0], "back"]
    elif standing:
        pygame.time.wait(1000)
        b.stand()
