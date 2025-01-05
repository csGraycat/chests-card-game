from deck import Deck
import os
import time
import random


def main():
    os.system('cls')
    ans = y_n_input("Play with Comp? (y/n) ")
    if ans == 'y' or ans == 'Y':
        mode = 1
    else:
        mode = 0
    if mode == 0:
        number_of_players = int_input("How many players? ")
    else:
        number_of_players = 2
    players = [[] for _ in range(number_of_players)]
    chest_counter = {player_id: 0 for player_id in range(number_of_players)}

    deck = Deck()
    print("Shuffling deck...")
    time.sleep(1)
    deck.shuffle()
    print("Cards are dealt")

    for player in players:
        player += deck.deal_from_top(5)
    for player_id, player_hand in enumerate(players):  # check if players have a chest initially
        player_hand = chest_collected(chest_counter, player_id, player_hand, mode)
        players[player_id] = player_hand

    time.sleep(1)
    while len(''.join(list(''.join(player) for player in players))) > 0:  # main game loop
        for player in enumerate(players):  # player[0] - player's id, player[1] - player's hand
            current_player_id = player[0]
            current_player_hand = player[1]
            ranks_chosen = []

            while True:
                players[current_player_id] = current_player_hand

                if mode == 0 or mode == 1 and current_player_id == 0:
                    if len(current_player_hand) > 0:
                        print("Player " + str(current_player_id + 1) + ", choose a rank from your hand")
                        print_cards(current_player_hand)
                    elif len(deck.cards) > 0:
                        print("Player " + str(current_player_id + 1) + " grabs a card from the deck")
                        new_card = deck.deal_from_top(1)[0]
                        current_player_hand.append(new_card)
                        print_cards(current_player_hand)
                        players[current_player_id] = current_player_hand
                        input("Press Enter to end the turn")
                        os.system('cls')
                        break
                    else:
                        #print("There are no more cards. Player " + str(current_player_id + 1) + " skips turn")
                        break
                else:
                    print_cards(players[0])
                    print("Comp's turn")
                    if len(current_player_hand) == 0:
                        if len(deck.cards) > 0:
                            print("Comp grabs a card from the deck")
                            new_card = deck.deal_from_top(1)[0]
                            current_player_hand.append(new_card)
                            players[current_player_id] = current_player_hand
                            input("Press Enter to end the turn")
                        os.system('cls')
                        break

                allowed_ranks = [x[:-1] for x in current_player_hand]
                if mode == 0 or mode == 1 and current_player_id == 0:
                    chosen_rank = player_choose_rank(allowed_ranks)
                    os.system('cls')
                else:
                    print("Comp picks a card to steal...")
                    chosen_rank = random.choice(allowed_ranks)
                    # print("allowed ranks ", allowed_ranks)
                    if chosen_rank not in ranks_chosen:
                        ranks_chosen.append(chosen_rank)
                    elif len(set(ranks_chosen)) < len(set(allowed_ranks)):
                        ranks_remaining = list(set(allowed_ranks) - set(ranks_chosen))
                        chosen_rank = random.choice(ranks_remaining)
                        # print("ranks remain ", ranks_remaining)
                    # print("ranks_chosen ", ranks_chosen)

                    time.sleep(1)
                    print(chosen_rank)

                    # print("comp cards")
                    # print_cards(players[current_player_id])

                    time.sleep(1)

                if number_of_players > 2:
                    steal_from_id = choose_steal_from(players, current_player_id)
                else:
                    steal_from_id = 1 if current_player_id == 0 else 0

                stolen_cards = []
                for card in players[steal_from_id]:
                    if card[:-1] == chosen_rank:
                        stolen_cards.append(card)

                if len(stolen_cards) > 0:

                    if mode == 0 or mode == 1 and current_player_id == 0:
                        print("You succesfully steal " + str(len(stolen_cards)) + " cards")
                        current_player_hand += stolen_cards
                        players[steal_from_id] = list(set(players[steal_from_id]) - set(stolen_cards))
                        current_player_hand = chest_collected(chest_counter, current_player_id, current_player_hand,
                                                              mode)
                        players[current_player_id] = current_player_hand
                        if len(''.join(
                                list(''.join(player) for player in players))) == 0 and mode == 1:
                            input("Press Enter to continue")

                    else:
                        print(f"Comp steals {len(stolen_cards)} cards from you")
                        current_player_hand += stolen_cards
                        players[steal_from_id] = list(set(players[steal_from_id]) - set(stolen_cards))
                        print_cards(players[steal_from_id])
                        current_player_hand = chest_collected(chest_counter, current_player_id, current_player_hand,
                                                              mode)
                        input("Press Enter to continue")
                        os.system('cls')
                else:
                    if mode == 0 or mode == 1 and current_player_id == 1:
                        print("Player " + str(steal_from_id + 1) + " does not have such cards")
                    else:
                        print("Comp does not have such cards")
                    if len(deck.cards) > 0:
                        new_card = deck.deal_from_top(1)[0]
                        if mode == 0 or mode == 1 and current_player_id == 0:
                            print("You grab a new card from the deck: ", new_card)
                        else:
                            print("Comp grabs a card from the deck")
                        current_player_hand.append(new_card)
                        current_player_hand = chest_collected(chest_counter, current_player_id, current_player_hand,
                                                              mode)
                        if mode == 0 or mode == 1 and current_player_id == 0:
                            print_cards(current_player_hand)
                    players[current_player_id] = current_player_hand

                    input("Press Enter to end the turn")
                    os.system('cls')
                    break

    os.system('cls')
    print("Game over")
    print("Chests collected:")
    if mode == 0:
        for player_id, chests in chest_counter.items():
            print(f"Player {player_id + 1} collected {chests}")
    if mode == 1:
        print(f"Player collected {list(chest_counter.items())[0][1]}")
        print(f"Comp collected {list(chest_counter.items())[1][1]}")


def int_input(prompt):
    while True:
        a = input(prompt)
        try:
            return int(a)
        except ValueError:
            print("Please enter a number")


def rank_counter(cards: list):
    counter = dict()
    for card in cards:
        try:
            counter[card[:-1]] += 1
        except KeyError:
            counter[card[:-1]] = 1
    return counter


def chest_collected(chest_counter, player_id, player_hand, mode):
    counter = rank_counter(player_hand)
    chest_rank = ""
    for item in counter.items():
        if item[1] == 4:
            chest_rank = item[0]
    if chest_rank:
        chest_counter[player_id] += 1  # chest_counter = {player_id: number_of_chests}
        player_hand = [card for card in player_hand if card[:-1] != chest_rank]
        if mode == 0 or mode == 1 and player_id == 0:
            print(f"You've collected a chest! {chest_rank}")
        else:
            time.sleep(1)
            print(f"Comp collected a chest!")
            time.sleep(1)
    return player_hand


def choose_steal_from(players: list, current_player_id):
    print("Choose a player to steal from")
    for opponent in enumerate(players):
        if opponent[0] != current_player_id:
            print("Player " + str(opponent[0] + 1))

    while True:
        chosen_opponent = int_input("")
        if chosen_opponent != current_player_id + 1 and 0 < chosen_opponent <= len(players):
            return chosen_opponent - 1
        else:
            print("Please enter a valid player number")


def print_cards(cards: list):
    if cards:
        line = ''
        current_rank = sorted(cards)[0][:-1]
        for card in sorted(cards):
            if card[:-1] == current_rank:
                line += card
                if card[:-1] != '10':
                    line += ' '
            else:
                print(line)
                line = card
                if card[:-1] != '10':
                    line += ' '
                current_rank = card[:-1]
        print(line)


def y_n_input(prompt):
    accept = ['y', 'Y', 'n', 'N']
    ans = ""
    while ans not in accept:
        ans = input(prompt)
    return ans


def player_choose_rank(allowed_ranks):
    while True:
        chosen_rank = input()
        if chosen_rank in allowed_ranks:
            return chosen_rank
        else:
            print("There is no such rank in your hand")


main()
