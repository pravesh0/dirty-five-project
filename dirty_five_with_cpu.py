import random, time


class Deck:
    def __init__(self):
        self.deck_cards = self.make_cards()
        self.cards_in_play = []

    # to generate all 52 cards
    def make_cards(self):
        cards = []
        for k in 'SHDC':
            for v in range(1, 14):
                cards.append((k, v))
        return cards

    # returns true if there are less than num cards in deck_card
    def is_remaining_cards(self, num):
        if len(self.deck_cards) < num:
            return True
        return False

    # num = number of cards to shuffle from the playing cards except this
    def reshuffle_cards(self, num):
        cards = []
        for card in self.cards_in_play[:-num]:
            if 0 not in card and -5 not in card:
                cards.append(card)

        random.shuffle(cards)
        for card in cards:
            self.deck_cards.append(card)
            self.cards_in_play.remove(card)
        random.shuffle(self.deck_cards)

    def get_random_cards(self, n):
        cards = random.sample(self.deck_cards, n)
        for card in cards:
            self.remove_card(card)
        return cards

    def remove_card(self, card):
        self.deck_cards.remove(card)

    def print_cards_in_play(self):
        print("\nLatest cards played on Table =========> [ ", end='')
        for card in self.cards_in_play[-5:]:
            if -5 not in card:
                print(card, end='')
        print(" ] <=======")


class Player:
    def __init__(self, p_id, cards):
        self.p_id = p_id
        self.cards = cards

    def get_cards(self):
        return self.cards

    def cards_with_aces(self, player_cards, k, v_moves, deck):
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
                    if not deck.cards_in_play:
                        v_moves.append([first_c])  # will append if its the first card to be played in game
                    elif deck.cards_in_play[-1][0] == k:
                        v_moves.append([first_c])

        return v_moves

    # Testing purposes
    def valid_cards_all(self, deck):
        cards = []
        for card in deck.cards_in_play[:]:
            if 0 not in card and -5 not in card:
                cards.append(card)
        return cards

    def get_valid_moves(self, deck):
        num = None
        v_moves = []
        player_cards = self.cards

        # if remaining cards are less than 14 and valid_cards_all smaller than 1 then reshuffle leaving last 6 cards
        if len(self.valid_cards_all(deck)) < 1 and deck.is_remaining_cards(14):
            for card in player_cards:
                if card[1] != 5 and card[1] != 11 and card[1] != 1:
                    v_moves = [[card]]
                    deck.reshuffle_cards(6)
                    return v_moves

        if len(deck.cards_in_play) == 0:
            k = 'S'
        else:
            last_card_played = deck.cards_in_play[-1]
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
                for card in deck.cards_in_play[-2::-1]:  # loop starts from second last card in played card
                    if card[1] == 5:
                        count += 2
                    else:
                        break
                m = 'penalty' + str(count)
                v_moves.append([m])
                return v_moves

        # when player doesn't want to play any card
        v_moves.append(['penalty1'])

        # for generating all the valid moves
        v_moves = self.cards_with_aces(player_cards, k, v_moves, deck)

        # match number
        for card in player_cards:
            if num == card[1] and card[1] == 1:
                self.cards_with_aces(player_cards, card[0], v_moves, deck)
            elif num == card[1] and card[1] != 1:
                v_moves.append([card])

        # for special case of J (11)
        for first_card in player_cards:
            if first_card[1] == 11 and [first_card] not in v_moves:
                v_moves.append([first_card])
        return v_moves

    # print valid moves
    def print_valid_moves(self, v_moves):
        print('\nCurrent Valid Options are: ')
        for i in range(len(v_moves)):
            # time.sleep(0.3)
            print('{} -> {}'.format(i + 1, v_moves[i]))
        print()

    def has_won(self):
        if len(self.cards) == 0:
            print('=' * 180)
            print("Player {} Won!".format(self.p_id))
            return True
        return False

    def play_move(self, v_moves, deck, pos=-1, j=None):
        # for choosing a move from the valid moves
        if pos == -1:
            while True:
                try:
                    pos = int(input("Choose which card to play and enter the position of the card: "))
                    if pos < 1 or pos > len(v_moves):
                        print("Incorrect input")
                        continue
                    else:
                        # time.sleep(0.3)
                        print(v_moves[pos - 1], "is selected to play")
                        break
                except ValueError:
                    print('Not a valid number! Try again')
            pos = pos - 1  # indexing starts from 0
        move = v_moves[pos]
        # get the cards that to be played (in c)
        c = []
        for single_card in move:
            if 'penalty' not in single_card:
                c.append(single_card)

        if deck.is_remaining_cards(14):
            deck.reshuffle_cards(4)

        if len(c) > 0:  # i.e, if c has cards
            # add the cards(in c) at the end of played cards list and remove that card from his hand
            for card in c:
                deck.cards_in_play.append(card)
                self.cards.remove(card)

            # special case for J (11)
            if not j:
                if c[-1][1] == 11:
                    choice = input('Please specify the kind of cards for the next moves: (S,H,D,C) :').strip().upper()
                    while True:
                        if choice not in ('S', 'H', 'D', 'C'):
                            print('Incorrect Input.Choose one from (s, h, d, c) only')
                            choice = input(
                                'Please specify the kind of cards for the next moves: (S,H,D,C) :').strip().upper
                        else:
                            print('You chose: ', choice)
                            break
                    deck.cards_in_play.append((choice, 0))
            else:
                deck.cards_in_play.append((j, 0))

        # for the penalty cards
        for p in move:
            if 'penalty' in p:
                num = int(p[7])  # no of penalty cards

                # check if there are n cards to pick
                try:
                    random_cards = random.sample(deck.deck_cards, num)
                except ValueError:
                    print("It will be considered a draw as no player is playing with spirit of game")
                    exit()

                # add the penalty cards to the hand
                for card in random_cards:
                    self.cards.append(card)
                # remove those penalty cards from deck_list
                for card in random_cards:
                    deck.deck_cards.remove(card)
                # when penalty was more than 1 card
                if num > 1:
                    last_card = deck.cards_in_play[-1]
                    if last_card and (last_card[0], -5) not in deck.deck_cards:
                        deck.cards_in_play.append((last_card[0], -5))

    def len_of_move(self, move, penalty=False):        # if penalty is True that means len with penalty
        if penalty:
            return len(move)
        if 'penalty' in move[-1]:
            return -1
        return len(move)

    # returns the no. of cards left of this kind, after playing the j_card
    def no_of_kinds(self, p_cards):
        counts = []
        for kind in 'SDHC':
            c = 0
            for card in p_cards:
                if card[1] == 11:
                    continue
                elif card[0] == kind:
                    c += 1
            else:
                counts.append(c)
        return counts

    # return the indices(all index) if the card/card_value/card_kind is found otherwise returns -1
    def return_index(self, v_moves, card=None, card_value=None, card_kind=None):
        indices = []
        for move in v_moves:
            for c in move:
                if card:
                    if c == card:
                        indices.append(v_moves.index(move))
                elif card_value:
                    if c[1] == card_value:
                        indices.append(v_moves.index(move))
                elif card_kind:
                    if c[0] == card_kind:
                        indices.append(v_moves.index(move))
        if indices != []:
            return indices
        return -1

    def play_auto(self, v_moves, deck):
        # when there is no other option to play but penalty
        if len(v_moves) == 1:
            self.play_move(v_moves, deck, pos=0)
            return

        if deck.cards_in_play != []:
            last_card = deck.cards_in_play[-1]
            # if last card was 5 and it has one or more 5
            if last_card[1] == 5 and self.return_index(v_moves, card_value=5) != -1:
                # pos_list will contain list of indices of cards with 5
                pos_list = self.return_index(v_moves, card_value=5)
                self.play_move(v_moves, deck, pos=random.choice(pos_list))
                return

        # if the len is longest and no penalty is involved
        maximum = [-1, -1]      # maximum[0] is len and max[1] is index of move
        for move in v_moves:
            if self.len_of_move(move) > maximum[0] and self.return_index([move], card_value=11) == -1:
                maximum[0] = self.len_of_move(move)
                maximum[1] = v_moves.index(move)
        if maximum[1] != -1:
            pos = maximum[1]
            self.play_move(v_moves, deck, pos)
            return

        # when it has one or more J to play... then select only that kind which have more in hand
        if self.return_index(v_moves, card_value=11) != -1:
            valid_move_indices = self.return_index(v_moves, card_value=11)

            # when it has one or more J than the move's index will be in pos
            pos = []
            for index in valid_move_indices:
                pos.append(index)

            counts = self.no_of_kinds(self.cards)
            max_index = counts.index(max(counts))


            if max_index == 0:
                self.play_move(v_moves, deck, pos=random.choice(pos), j='S')
                return
            if max_index == 1:
                self.play_move(v_moves, deck, pos=random.choice(pos), j='D')
                return
            if max_index == 2:
                self.play_move(v_moves, deck, pos=random.choice(pos), j='H')
                return
            if max_index == 3:
                self.play_move(v_moves, deck, pos=random.choice(pos), j='C')
                return

        self.play_move(v_moves, deck, pos=0)
        return

    # returns True if last card
    def is_last_card(self, deck):
        moves = []
        c = []
        if len(self.cards) == 1:
            print()
            print('-'*20, 'PLAYER {} LAST CARD'.format(self.p_id), '-'*20)
            return True
        for card in self.cards:
            if card[0] not in c:
                moves = self.cards_with_aces(self.cards, card[0], moves, deck)
                c.append(card[0])

        for move in moves:
            if len(move) == len(self.cards) and 'penalty1' not in move:
                print()
                print('-' * 20, 'PLAYER {} LAST CARD'.format(self.p_id), '-' * 20)
                return True

        return False


class Game:
    def __init__(self):
        self.no_of_players = 2
        self.deck = Deck()
        self.player_list = self.generate_players(self.no_of_players)
        self.game_id = None

    def input_players(self):
        while True:
            try:
                num = int(input("Enter number of players between 2 and 6: "))
                if not (num < 2 or num > 6):
                    return num
                print("Incorrect_input")
                continue
            except ValueError:
                print('Not a number! Please enter numbers only')

    def generate_players(self, num):
        p = list('ABCDEFGH')
        players = []
        for i in range(0, num):
            cards = self.deck.get_random_cards(5)  # Deal Card to Player
            player = Player(p[i], cards)  # Save Player ID and Card
            players.append(player)
        return players

    def return_hand_cards(self):
        cards = []
        for player in self.player_list:
            cards.append(player.get_cards())
        return cards

    def get_first_player(self):
        current_hand_cards = self.return_hand_cards()
        temp = ('S', 0)
        for hand in current_hand_cards:
            for card in hand:
                if card == ('S', 1):  # for checking ace of spades
                    f = current_hand_cards.index(hand)
                    return self.player_list[f]
                elif 'S' in card:  # for comparing the highest spade card
                    if card[1] > temp[1]:
                        temp = card

        if temp == ('S', 0):  # True if no player got any spade cards
            return random.choice(self.player_list)

        for hand in current_hand_cards:  # Based on higher spade card
            if temp in hand:
                f = current_hand_cards.index(hand)
                return self.player_list[f]

    def get_next_player(self, curr_player):
        if self.player_list.index(curr_player) == len(self.player_list) - 1:
            next_player = self.player_list[0]
        else:
            next_player = self.player_list[self.player_list.index(curr_player) + 1]
        return next_player

    def show_hand_cards(self):
        print("\nCards in each player's hand")
        for i in range(self.no_of_players):
            print(self.player_list[i].p_id, '==>', self.player_list[i].cards)
        print()

    def run(self):
        curr_player = self.get_first_player()

        while True:

            print()
            self.deck.print_cards_in_play()

            if curr_player.p_id == "A":
                time.sleep(0.5)
                valid_moves = curr_player.get_valid_moves(self.deck)
                curr_player.play_auto(valid_moves, self.deck)
                curr_player.is_last_card(self.deck)
                if curr_player.has_won():
                    break
                curr_player = self.get_next_player(curr_player)
                self.show_hand_cards()

                self.deck.print_cards_in_play()

            print("Your's turn".format(curr_player.p_id))
            print("{} ==> {}".format(curr_player.p_id, curr_player.get_cards()))
            valid_moves = curr_player.get_valid_moves(self.deck)
            curr_player.print_valid_moves(valid_moves)

            curr_player.play_move(valid_moves, self.deck)
            curr_player.is_last_card(self.deck)
            if curr_player.has_won():
                break

            curr_player = self.get_next_player(curr_player)


if __name__ == "__main__":
    game1 = Game()
    game1.run()
