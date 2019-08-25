import time
import random

deck_list = []
cards_in_play = []  # cards which are being played

for ch in 'dcsh':
    for v in range(1, 14):
        deck_list.append((ch, v))


def input_no_of_players():
    while True:
        try:
            num = int(input("Enter number of players between 2 and 6: "))
            if not (num < 2 or num > 6):
                return num
            print("Incorrect_input")
            continue
        except ValueError:
            print('Not a number! Please enter numbers only')


# function for dealing the cards
def initial_deal(num):
    h_cards = []
    for i in range(num):
        rn_cards = random.sample(deck_list, 5)
        h_cards.append(rn_cards)

        for card in rn_cards:
                deck_list.remove(card)

    return h_cards


# for assigning the symbols of players to a list
def assign_symbols(num):
    p = list('ABCDEFGH')
    p_symbols = []

    for i in range(num):
        p_symbols.append(p[i])
    return p_symbols


def return_next_symbol(curr_symbol, p_symbols):
    if p_symbols.index(curr_symbol) == (len(p_symbols) - 1):
        next_symbol = p_symbols[0]
    else:
        next_symbol = p_symbols[p_symbols.index(curr_symbol) + 1]

    return next_symbol


def return_player_cards(curr_symbol):
    player_index = player_symbols.index(curr_symbol)
    player_cards = hand_cards[player_index]
    return player_cards


# check if there are enough cards left after penalty cards are given
def remaining_deck_cards(num):

    if len(deck_list) < num:
        return True
    return False


def reshuffle_cards(num):       # num = number of cards to shuffle from the playing cards except this
    cards = []
    for card in cards_in_play[:-num]:
        if 0 not in card and -5 not in card:
            cards.append(card)

    random.shuffle(cards)
    for card in cards:
        deck_list.append(card)
        cards_in_play.remove(card)

    random.shuffle(deck_list)


# playing the card with single penalty card
def playing_with_penalty(move, player_index):

    # get the cards that to be played (in c)
    c = []
    for single_card in move:
        if 'penalty' not in single_card:
            c.append(single_card)

    if  remaining_deck_cards(9):
        reshuffle_cards(4)

    if len(c) > 0:  # i.e, if c has cards
        # add the cards(in c) at the end of played cards list and remove that card from his hand
        for card in c:
            cards_in_play.append(card)
            hand_cards[player_index].remove(card)

        # special case for J (11)
        if c[-1][1] == 11:
            choice = input('Please specify the kind of cards for the next moves: (s,h,d,c) :').strip().lower()
            while True:
                if choice not in ('s', 'h', 'd', 'c'):
                    print('Incorrect Input.Choose one from (s, h, d, c) only')
                    choice = input('Please specify the kind of cards for the next moves: (s,h,d,c) :').strip().lower()
                else:
                    print('You chose: ', choice)
                    break

            cards_in_play.append((choice, 0))



    # for the penalty cards
    for p in move:
        if 'penalty' in p:
            num = int(p[7])  # no of penalty cards

            # check if there are n cards to pick
            try:

                random_cards = random.sample(deck_list, num)
            
            except ValueError:
            	print("It will be considered a draw as no player is playing with spirit of game")
            	exit()

            # add the penalty cards to the hand
            for card in random_cards:
                hand_cards[player_index].append(card)

            # remove those penalty cards from deck_list
            for card in random_cards:
                deck_list.remove(card)
            # when penalty was more than 1 card
            if num > 1:
                last_card = cards_in_play[-1]
                if last_card and (last_card[0], -5) not in deck_list:
                    cards_in_play.append((last_card[0], -5))


# deciding who will get the first move
def return_first_move_symbol(current_hand_cards, symbols):
    temp = ('s', 0)
    for hand in current_hand_cards:
        for card in hand:
            if card == ('s', 1):  # for checking ace of spades
                f = current_hand_cards.index(hand)
                return symbols[f]
            elif 's' in card:  # for comparing the highest spade card
                if card[1] > temp[1]:
                    temp = card

    if temp == ('s', 0):  # True if no player got any spade cards
        return random.choice(symbols)

    for hand in current_hand_cards:  # Based on higher spade card
        if temp in hand:
            f = current_hand_cards.index(hand)
            return symbols[f]


def match_number(num, p_cards, v_moves):
    for card in p_cards:
        if num == card[1] and card[1] == 1:
        	cards_with_aces(p_cards, card[0], v_moves)
        elif num == card[1] and card[1] != 1:
            v_moves.append([card])
    return v_moves


def cards_with_aces(player_cards, k, v_moves):
    for first_c in player_cards:
        if k in first_c:  # spade cards are present
            if 1 in first_c:  # ace of spade is present
                # for testing
                if [first_c, 'penalty1'] not in v_moves:
                    v_moves.append([first_c, 'penalty1'])

                # code for choosing another card - probably function
                for second_c in player_cards:

                    # when we have 2th card as same as kind of 1st ace
                    if first_c[0] == second_c[0] and (first_c != second_c):
                        v_moves.append([first_c, second_c])

                    # condition will be true if there is 2nd aces
                    if (1 in second_c) and (k not in second_c):

                        # testing
                        if [first_c, second_c, 'penalty1'] not in v_moves:
                            v_moves.append([first_c, second_c, 'penalty1'])

                        for third_c in player_cards:

                            # when we have 3th card as same as kind of 2rd ace
                            if second_c[0] == third_c[0] and second_c != third_c:
                                v_moves.append([first_c, second_c, third_c])

                            # condition will be true if there is 3rd ace
                            if (1 in third_c) and (k not in third_c) and (second_c[0] not in third_c):

                                for fourth_c in player_cards:

                                    # testing
                                    if [first_c, second_c, third_c, 'penalty1'] not in v_moves:
                                        v_moves.append([first_c, second_c, third_c, 'penalty1'])

                                    # when we have 4th card as same as kind of 3rd ace
                                    if third_c[0] == fourth_c[0] and third_c != fourth_c:
                                        v_moves.append([first_c, second_c, third_c, fourth_c])

                                    # condition will be true if there is 4th ace
                                    if (1 in fourth_c) and (k not in fourth_c) and (
                                            second_c[0] not in fourth_c) and (third_c[0] not in fourth_c):

                                        # testing
                                        if [first_c, second_c, third_c, fourth_c, 'penalty1'] not in v_moves:
                                            v_moves.append(
                                                [first_c, second_c, third_c, fourth_c, 'penalty1'])

                                        for fifth_c in player_cards:

                                            # when we have 5th card as same as kind of 4th ace
                                            if fourth_c[0] == fifth_c[0] and fourth_c != fifth_c:
                                                v_moves.append(
                                                    [first_c, second_c, third_c, fourth_c, fifth_c])

            # if first card is of spades but not ace
            else:
                v_moves.append([first_c])
    return v_moves


def return_valid_moves(curr_symbol):
    num = None
    v_moves = []
    player_cards = return_player_cards(curr_symbol)

    # for special case when no more than 2 cards are there yet and len(deck_list) < 5
    if len(valid_cards_all()) < 1 and remaining_deck_cards(14):
        for card in player_cards:
            if card[1] != 5 and card[1] != 11 and card[1] !=1:
                v_moves = [[card]]
                reshuffle_cards(6)
                return v_moves


    if len(cards_in_play) == 0:
        k = 's'
    else:
        last_card_played = cards_in_play[-1]
        k = last_card_played[0]
        num = abs(last_card_played[1])  # converts -5 to 5 for comparision with last card

        # for special case of 5
        if last_card_played[1] == 5:
            count = 2
            # valid_moves.append(['penalty2'])
            # for checking if player has 5
            for card in player_cards:
                if card[1] == 5:
                    v_moves.append([card])

            # for checking the how many consecutive 5 were played and deciding no.of penalty cards on that basis
            for card in cards_in_play[-2::-1]:  # loop starts from second last card in played card
                if card[1] == 5:
                    count += 2
                else:
                    m = 'penalty' + str(count)
                    v_moves.append([m])
                    return v_moves

            v_moves.append(['penalty2'])
            return v_moves

    # when player doesn't want to play any card
    v_moves.append(['penalty1'])

    # for generating all the valid moves
    v_moves = cards_with_aces(player_cards, k, v_moves)
    v_moves = match_number(num, player_cards, v_moves)

    # for special case of J (11)
    for first_card in player_cards:
        if first_card[1] == 11 and [first_card] not in v_moves:
            v_moves.append([first_card])

    return v_moves


def play_move(v_moves, curr_symbol):
    # for choosing a move from the valid moves
    while True:
        try:
            pos = int(input("Choose which card to play and enter the position of the card: "))
            if pos < 0 or pos > len(v_moves):
                print("Incorrect input")

                continue
            else:
                # time.sleep(0.3)
                print(v_moves[pos - 1], "is selected to play")
                break
        except ValueError:
            print('Not a valid number! Try again')
    pos = pos - 1  # indexing starts from 0

    playing_with_penalty(v_moves[pos], player_symbols.index(curr_symbol))


def print_hand_cards():
    print("\nCards in each player's hand")
    for i in range(no_of_players):
        # time.sleep(0.3)
        print(player_symbols[i], '==>', hand_cards[i])
    print()


def is_win(s):
    for i in range(no_of_players):
        if len(hand_cards[i]) == 0:
            print('=' * 180)
            print("Player {} Won!".format(s))
            return True
    return False


# print valid moves
def print_valid_moves(v_moves):
    print('\nCurrent Valid Options are: ')
    for i in range(len(v_moves)):
        # time.sleep(0.3)
        print('{} -> {}'.format(i + 1, v_moves[i]))
    print()


def print_cards_in_play(cards):
    print("\nLatest cards played on Table =========> [ ", end='')
    for card in cards[-5:]:
        if -5 not in card:
            print(card, end='')
    print(" ] <=======")

# Testing
def valid_cards_6():
    cards = []
    for card in cards_in_play[:-5]:
        if 0 not in card and -5 not in card:
            cards.append(card)
    return cards


# Testing
def valid_cards_all():
    cards = []
    for card in cards_in_play[:]:
        if 0 not in card and -5 not in card:
            cards.append(card)
    return cards


no_of_players = input_no_of_players()

player_symbols = assign_symbols(no_of_players)

# dealing the cards
hand_cards = initial_deal(no_of_players)

# decide who will go first
symbol = return_first_move_symbol(hand_cards, player_symbols)

while True:

    # printing the hand cards
    print_hand_cards()
    
   
    # testing - try to tun like multiplayer on console
    print('\n' *40)
    print_cards_in_play(cards_in_play)
    print("{}'s turn".format(symbol))
    print("{} ==> {}".format(symbol,return_player_cards(symbol)))
    valid_moves = return_valid_moves(symbol)
    print_valid_moves(valid_moves)

    play_move(valid_moves, symbol)
    
    # testing - for console multiplayer
    print('\n' *40)
    time.sleep(2)
    
    #print(
#    "TESTING no of cards in cards_play {} , no of valid_cards_play_6 {}, no of valid_cards_play_all {}, no of cards in deck_list {}".format(
#        len(cards_in_play), len(valid_cards_6()), len(valid_cards_all()), len(deck_list)))
#    print(
#    "TESTING cards in cards_play {} \n, valid_cards_play_6 {}\n valid_cards_play_all {}\ncards in deck_list {}".format(
#        cards_in_play, valid_cards_6(), valid_cards_all(), deck_list))

# check for win
    if is_win(symbol):
        break
    # time.sleep(0.3)

    
    # decide who will play next move
    symbol = return_next_symbol(symbol, player_symbols)
