suit = {
    "S": 1,
    "H": 2,
    "D": 3,
    "C": 4}
def card_coordinates(card):
    length = 1200
    width = 544
    card_suit = card[0]
    if len(card) == 2:
        card_value = int(card[1])
    else:
        card_value = int(card[1] + card[2])
    card_suit = suit[card_suit]
    x_coordinate = length // 13 * (card_value - 1)
    y_coordinate = width // 4 * (card_suit - 1)
    return (x_coordinate, y_coordinate)

import random
import pygame
pygame.init()
screen = pygame.display.set_mode(size=(800,600))
image = pygame.image.load("cards.png")

number_of_players = int(input())
def shuffle_deck():
    cards_deck = []
    suits = ["C", "S", "H", "D"]
    for i in range(1, 14):
        for i2 in range(4):
            cards_deck.append(suits[i2] + str(i))
    random.shuffle(cards_deck)
    return cards_deck
#TODO more than one deck, max number of players
all_player_decks = []
shuffled = shuffle_deck()
# separating the cards into player decks
for i3 in range(1, number_of_players + 1):
    player_deck = []
    lower = (i3 - 1) * 8
    upper = i3 * 8
    middle_card = []
    middle_card.append(shuffled[upper])
    shuffled.pop(upper)
    for i4 in range(lower, upper):
        player_deck.append(shuffled[i4])
        shuffled.pop(i4)
    all_player_decks.append(player_deck)
print(all_player_decks)
print(middle_card)

card_width = 1200 // 13
card_length = 544 // 4

#centering the player deck on the bottom of the screen
def x_center_player_deck(player_deck_number):
    x_coord = []
    x_first_card = (800 - (len(all_player_decks[player_deck_number]) * card_width)) / 2
    for i5 in range(len(all_player_decks[player_deck_number])):
        x_coord.append(x_first_card + i5 * card_width)
    return x_coord


def game():
    player_number = 0
    while True:
        x_coordinates = (x_center_player_deck(player_number))
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                for i7 in range(len(all_player_decks[player_number])):
                    if pygame.mouse.get_pos()[0] > x_coordinates[i7] and pygame.mouse.get_pos()[0] < (x_coordinates[i7] + card_width) and pygame.mouse.get_pos()[1] > 464:
                        if all_player_decks[player_number][i7][0] == middle_card[len(middle_card) - 1][0] and all_player_decks[player_number][i7][1] == "8":
                            print("spades, hearts, diamonds, or clubs?")
                            middle_card.append(all_player_decks[player_number][i7])
                            all_player_decks[player_number].pop(i7)
                            choose_suit = input()
                            if choose_suit == "spades":
                                middle_card.append("S8")
                            elif choose_suit == "hearts":
                                middle_card.append("H8")
                            elif choose_suit == "diamonds":
                                middle_card.append("D8")
                            elif choose_suit == "clubs":
                                middle_card.append("C8")
                            player_number += 1
                            player_number %= number_of_players

                        if len(all_player_decks[player_number][i7]) == 3:
                            if all_player_decks[player_number][i7][0] == middle_card[len(middle_card) - 1][0] or (len(middle_card[len(middle_card) - 1]) == 3 and all_player_decks[player_number][i7][1] + all_player_decks[player_number][i7][2] == middle_card[len(middle_card) - 1][1] + middle_card[len(middle_card) - 1][2]):
                                print(all_player_decks[player_number][i7])
                                middle_card.append(all_player_decks[player_number][i7])
                                all_player_decks[player_number].pop(i7)
                                player_number += 1
                                player_number %= number_of_players
                        elif len(all_player_decks[player_number][i7]) == 2:
                            if all_player_decks[player_number][i7][0] == middle_card[len(middle_card) - 1][0] or (len(middle_card[len(middle_card) - 1]) < 3 and all_player_decks[player_number][i7][1] == middle_card[len(middle_card) - 1][1]):
                                print(all_player_decks[player_number][i7])
                                middle_card.append(all_player_decks[player_number][i7])
                                all_player_decks[player_number].pop(i7)
                                player_number += 1
                                player_number %= number_of_players

                        if len(all_player_decks[player_number]) == 0:
                            print("You have won")

                if pygame.mouse.get_pos()[0] > 400 and pygame.mouse.get_pos()[0] < 400 + card_width and pygame.mouse.get_pos()[1] > 300 - card_length and pygame.mouse.get_pos()[1] < 300:
                    all_player_decks[player_number].append(shuffled[0])
                    shuffled.pop(0)
                    player_number += 1
                    player_number %= number_of_players
                    if len(shuffled) == 0:
                        for i6 in range(len(middle_card)-1):
                            shuffled.append(middle_card[0])
                            middle_card.pop(0)
                            random.shuffle(shuffled)
                print(pygame.mouse.get_pos())
        # drawing player decks
        x_coordinates = (x_center_player_deck(player_number))
        for i7 in range(len(all_player_decks[player_number])):
            coordinates = card_coordinates(all_player_decks[player_number][i7])
            screen.blit(image, (x_coordinates[i7], 464),
                        (coordinates[0], coordinates[1], card_width, card_length))
        # drawing middle card
        coordinates = card_coordinates(middle_card[len(middle_card) - 1])
        screen.blit(image, (400 - card_width, 300 - card_length),
                    (coordinates[0], coordinates[1], card_width, card_length))
        # drawing "pick-up" plie of cards
        pygame.draw.rect(screen, (0, 100, 175), (400, 300 - card_length, card_width, card_length))
        pygame.display.update()

game()
