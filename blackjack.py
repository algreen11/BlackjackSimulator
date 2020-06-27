import random
import numpy as np
import pandas as pd
import multiprocessing

# matrices that show moves based on cards: 0 = stick, 1 = hit, 2 =
# doubledown, 3 = split

# hard total matrix, top column is dealer card, rows denoted by total of
# user hand
data = np.array([['', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14'],
                 ['4', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 ['5', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 ['6', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 ['7', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 ['8', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 ['9', 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1],
                 ['10', 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1],
                 ['11', 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
                 ['12', 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                 ['13', 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                 ['14', 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                 ['15', 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                 ['16', 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]])
hard_total = pd.DataFrame(data=data[1:, 1:],
                          index=data[1:, 0],
                          columns=data[0, 1:])

# soft total matrix
data = np.array([['', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14'],
                 # remove this line when add split logic
                 ['12', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                 ['13', 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1],
                 ['14', 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1],
                 ['15', 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1],
                 ['16', 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1],
                 ['17', 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1],
                 ['18', 0, 2, 2, 2, 2, 0, 0, 1, 1, 1, 1, 1, 1],
                 ['19', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 ['20', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 ['21', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
soft_total = pd.DataFrame(data=data[1:, 1:],
                          index=data[1:, 0],
                          columns=data[0, 1:])

# split matrix
data = np.array([['', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14'],
                 # remove this line when add split logic
                 ['4', 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1],
                 ['6', 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1],
                 ['8', 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1],
                 ['10', 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1],
                 ['12', 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1],
                 ['14', 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1],
                 ['16', 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                 ['18', 3, 3, 3, 3, 3, 0, 3, 3, 0, 0, 0, 0, 0],
                 ['20', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
split = pd.DataFrame(data=data[1:, 1:],
                     index=data[1:, 0],
                     columns=data[0, 1:])


class BlackjackSim:

    def __init__(self):
        # Counting cards: keep running count of high/low cards seen
        self.count = 0

    def shuffle_deck(self):  # d - diamonds, h - hearts, s - spades, c - clubs
        deck = [[2, 'd'], [3, 'd'], [4, 'd'], [5, 'd'], [6, 'd'], [7, 'd'], [8, 'd'], [9, 'd'], [10, 'd'], [11, 'd'], [12, 'd'], [13, 'd'], [14, 'd'],
                [2, 'h'], [3, 'h'], [4, 'h'], [5, 'h'], [6, 'h'], [7, 'h'], [8, 'h'], [9, 'h'], [10, 'h'], [11, 'h'], [12, 'h'], [13, 'h'], [14, 'h'],
                [2, 's'], [3, 's'], [4, 's'], [5, 's'], [6, 's'], [7, 's'], [8, 's'], [9, 's'], [10, 's'], [11, 's'], [12, 's'], [13, 's'], [14, 's'],
                [2, 'c'], [3, 'c'], [4, 'c'], [5, 'c'], [6, 'c'], [7, 'c'], [8, 'c'], [9, 'c'], [10, 'c'], [11, 'c'], [12, 'c'], [13, 'c'], [14, 'c'],
                ]

        shuffled = deck * 6

        random.shuffle(shuffled)

        return shuffled[:]

    def play_hand(self, deck):

        dealer_hand = []
        user_hand = []
        doubled_down = False
        split = False

        bet = self.place_bet()

        # if count is negative don't bet, but simulate other 
        # cards being played to keep count moving
        if (bet == 0):
            for x in range(random.randint(4, 10)):
                card = deck.pop()
                self.change_count(card)
            return 0, 0, 0


        # give cards to player and dealer
        for x in range(4):
            card = deck.pop()
            self.change_count(card)
            if x % 2 == 0:
                user_hand.append(card)
            else:
                dealer_hand.append(card)

        # hit or stick for both player and dealer, don't do anything with
        # blackjack
        if not ((self.total(user_hand) == 21 and self.total(dealer_hand) != 21)):
            doubled_down, split = self.hit_or_stick_player(
                deck, user_hand, dealer_hand[1])
            # if split or bust don't deal to dealer
            if self.total(user_hand) < 22 and split is False:
                self.hit_or_stick_dealer(deck, dealer_hand)

        if split is False:
            return self.score_hand(user_hand, dealer_hand, doubled_down, bet)
        else: # play out split hands
            winnings, losses, draws = 0, 0, 0
            hands = []
            for card in user_hand:
                hand = [card, deck.pop()]
                doubled_down, split = self.hit_or_stick_player(
                    deck, hand, dealer_hand[1])  # allows for one extra split
                if split:
                    for crd in hand:
                        hnd = [crd, deck.pop()]
                        # should make it so that player doesn't have option to
                        # split again
                        doubled_down, split = self.hit_or_stick_player(
                            deck, hnd, dealer_hand[1])
                        hands.append([hnd, doubled_down])
                else:
                    hands.append([hand, doubled_down])

            self.hit_or_stick_dealer(deck, dealer_hand)
            for hand in hands:
                w, d, l = self.score_hand(hand[0], dealer_hand, hand[1], bet)
                if w == 1.5:
                    w = 1  # don't get blackjack bonus after splitting
                winnings += w
                losses += l
                draws += d

            return winnings, draws, losses

    def score_hand(self, user_hand, dealer_hand, doubled_down, bet):
        winnings = 0
        draws = 0
        losses = 0

        user = self.total(user_hand)
        dealer = self.total(dealer_hand)

        if user > 21:
            losses = 1
        elif user > dealer or dealer > 21:
            if len(user_hand) == 2 and user == 21:  # blackjack
                winnings += 1.5
            else:
                winnings += 1
        elif dealer > user:
            losses = 1
        else:
            draws += 1

        if doubled_down is True and draws < 1:
            if winnings == 0:
                losses = 2
            else:
                winnings = 2

        return winnings * bet, draws, losses * bet

    def hit_or_stick_dealer(self, deck, hand):
        tot = self.total(hand)
        while tot < 17 and not tot > 22:
            card = deck.pop()
            self.change_count(card)
            hand.append(card)
            tot = self.total(hand)

    # returns true if doubled down
    def hit_or_stick_player(self, deck, hand, dealer_card):
        tot = self.total(hand)
        while True:
            move = self.hit_logic(deck, hand, tot, dealer_card)
            if move == 1:
                card = deck.pop()
                self.change_count(card)
                hand.append(card)
                tot = self.total(hand)
            elif move == 2:
                return True, False
            elif move == 3:
                return False, True
            else:
                return False, False

    def change_count(self, card):
        if card[0] < 7:
            self.count -= 1
        elif card[0] > 9:
            self.count += 1

    def place_bet(self):
        true_count = int(self.count / 6)
        return max(0, 5 + 5 * true_count)

    def hit_logic(self, deck, hand, total, dealer_card):
        soft = [card for card in hand if card[0] == 14]
        if len(hand) == 2 and len(soft) == 1:  # have a soft total
            move = int(soft_total.loc[str(total)][str(dealer_card[0])])
        elif len(hand) == 2 and hand[0][0] == hand[1][0]:  # split
            # if 2 aces always split - total function doesn't pick up diff
            # between A,A and 6,6
            if hand[0][0] == 14:
                move = 3
            else:
                move = int(split.loc[str(total)][str(dealer_card[0])])
        elif total > 16:  # stick
            return 0
        else:  # hard total
            move = int(hard_total.loc[str(total)][str(dealer_card[0])])


        if move == 1:  # hit
            return 1
        elif move == 2:  # doubledown
            if len(hand) == 2:
                card = deck.pop()
                hand.append(card)
                return 2
            else:
                return 1
        elif move == 3:  # split
            return 3
        else:  # stand
            return 0

    def total(self, hand):
        tot = 0
        is_ace = False
        for x in hand:
            num = x[0]
            if num > 10 and num < 14:
                num = 10
            elif num == 14:
                if tot <= 10:
                    num = 11
                    is_ace = True
                else:
                    num = 1
            tot += num
        if is_ace and tot > 21:
            tot = 0
            for x in hand:
                num = x[0]
                if num > 10 and num < 14:
                    num = 10
                elif num == 14:
                    num = 1
                tot += num
        return tot

    def black_jack(self):
        winnings = 0
        draws = 0
        losses = 0
        hands = 0
        while hands < 100000:
            self.count = 0
            deck = self.shuffle_deck()

            while len(deck) > 78:  # 75% of deck played
                win, draw, loss = self.play_hand(deck)
                winnings += win
                draws += draw
                hands += 1
                losses += loss

        return winnings, losses, draws, hands


def class_wrapper():
    game = BlackjackSim()
    return game.black_jack()


if __name__ == '__main__':
    # multiply by 100k to get amount of hands to play
    amount_to_run = 8

    # execute blackjack function in parallel
    pool = multiprocessing.Pool()
    results = pool.starmap_async(
        class_wrapper, [() for _ in range(amount_to_run)])
    pool.close()
    pool.join()

    # format results
    results = results.get()
    results = [sum(x) for x in zip(*results)]
    winnings = results[0]
    losses = results[1]
    draws = results[2]
    hands = results[3]

    print("Won $%d and lost $%d over %d hands for percentage winnings of %f" %
          (winnings, losses, hands, float(winnings - losses) / hands))
    print("Had %d draws over %d hands as well" % (draws, hands))
