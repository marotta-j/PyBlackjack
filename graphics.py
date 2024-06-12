import pygame # TODO: Rewrite this whole file ( Fix main.py first)
import os
import main

# Initialize Pygame
pygame.init()


font = pygame.font.Font('freesansbold.ttf', 40)  # Normal Font
small_font = pygame.font.Font('freesansbold.ttf', 20)  # Smaller Font

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 128, 0)  # Green background
CARD_WIDTH, CARD_HEIGHT = 91, 116  # Typical card dimensions
CARD_GAP = 20  # Space between cards

# Paths
CARD_IMAGES_PATH = "cards"  # Update this path

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack Dealer's Table")

# Load card images
def load_card_image(card_name):
    card_image = pygame.image.load(os.path.join(CARD_IMAGES_PATH, f"{card_name}.png"))
    return pygame.transform.scale(card_image, (CARD_WIDTH, CARD_HEIGHT))

b = main.BlackJackGame()
b.deal()
player_hand = b.playerCards
dealer_hand = [b.dealerCards[0]]

# Function to display a hand of cards
def display_hand(hand, start_x, start_y):
    for i, card in enumerate(hand):
        card_image = load_card_image(card)
        screen.blit(card_image, (start_x + i * (CARD_WIDTH + CARD_GAP), start_y))


def reset():
    global player_hand, dealer_hand
    b.deal()
    player_hand = b.playerCards
    dealer_hand = [b.dealerCards[0]]

def lossMsg(status):
    if status == 0:
        return "Push"
    elif status == 0.5:
        return "You WIN!"
    elif status == 1:
        return "You WIN!"
    elif status == -1:
        return "You LOSE"

# Main loop
running = True
standing = False
endMsg = ""
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == "return":
                endMsg = lossMsg(b.hit())
            if pygame.key.name(event.key) == "space":
                dealer_hand = b.dealerCards
                standing = True

    screen.fill(BACKGROUND_COLOR)

    # Display player's hand
    player_start_x = (SCREEN_WIDTH - (len(player_hand) * (CARD_WIDTH + CARD_GAP) - CARD_GAP)) // 2
    display_hand(player_hand, player_start_x, 400)

    # Display dealer's hand
    dealer_start_x = (SCREEN_WIDTH - (len(dealer_hand) * (CARD_WIDTH + CARD_GAP) - CARD_GAP)) // 2
    display_hand(dealer_hand, dealer_start_x, 100)

    screen.blit(font.render(str(b.sum(b.playerCards)), True, (255, 255, 255)), (350, 540))
    if standing:
        screen.blit(font.render(str(b.sum(b.dealerCards)), True, (255, 255, 255)), (350, 250))

    if b.gameOver:
        screen.blit(font.render(endMsg, True, (0, 0, 0)), (30, 540))
        dealer_start_x = (SCREEN_WIDTH - (len(dealer_hand) * (CARD_WIDTH + CARD_GAP) - CARD_GAP)) // 2
        display_hand(dealer_hand, dealer_start_x, 100)
        pygame.display.update()
        pygame.time.wait(4000)
        standing = False
        reset()

    # Update the display
    pygame.display.flip()

    if standing:
        pygame.time.wait(2000)
        endMsg = lossMsg(b.stand())

# Quit Pygame
pygame.quit()
