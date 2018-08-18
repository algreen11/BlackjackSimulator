import random

def shuffleDeck():  # d - diamonds, h - hearts, s - spades, c - clubs
    deck = [[2, 'd'], [3, 'd'], [4, 'd'], [5, 'd'], [6, 'd'], [7, 'd'], [8, 'd'], [9, 'd'], [10, 'd'], [11, 'd'], [12, 'd'], [13, 'd'], [14, 'd'], 
            [2, 'h'], [3, 'h'], [4, 'h'], [5, 'h'], [6, 'h'], [7, 'h'], [8, 'h'], [9, 'h'], [10, 'h'], [11, 'h'], [12, 'h'], [13, 'h'], [14, 'h'],
            [2, 's'], [3, 's'], [4, 's'], [5, 's'], [6, 's'], [7, 's'], [8, 's'], [9, 's'], [10, 's'], [11, 's'], [12, 's'], [13, 's'], [14, 's'],
            [2, 'c'], [3, 'c'], [4, 'c'], [5, 'c'], [6, 'c'], [7, 'c'], [8, 'c'], [9, 'c'], [10, 'c'], [11, 'c'], [12, 'c'], [13, 'c'], [14, 'c'],
            ]

    shuffled = deck * 6

    random.shuffle(shuffled)

    return shuffled[:]

def playHand(deck):
    winnings = 0
    draws = 0
    dealerHand = []
    userHand = []
    for x in range(4):
        if x % 2 == 0:
            userHand.append(deck.pop())
        else:
            dealerHand.append(deck.pop())

    if total(userHand) != 21 or total(dealerHand) != 21: 
        hitOrStick(deck, userHand)
        if total(userHand) < 22:
            hitOrStick(deck, dealerHand)

    print("user hand:", total(userHand), userHand)
    print("dealer hand:", total(dealerHand), dealerHand)

    user = total(userHand)
    dealer = total(dealerHand)

    if user > 21:
        None 
        #winnings -= 1
    elif user > dealer or dealer > 21:
        winnings += 1
    elif dealer > user:
        None 
        #winnings -= 1
    else:
        draws += 1
    print(winnings, draws)
    return winnings, draws


def hitOrStick(deck, hand):
    tot = total(hand)
    while tot < 17 and not tot > 22:
        card = deck.pop()
        hand.append(card)
        tot = total(hand)
    #print(tot)

def total(hand):
    tot = 0
    isAce = False 
    for x in hand:
        num = x[0]
        if num > 10 and num < 14:
            num = 10
        elif num == 14:
            if tot <= 10: 
                num = 11
                isAce = True
            else: 
                num = 1
        tot += num
    if isAce and tot > 21:
        tot = 0
        for x in hand:
            num = x[0]
            if num > 10 and num < 14:
                num = 10
            elif num == 14:
                num = 1
            tot += num
    return tot

def blackJack():
    winnings = 0
    draws = 0
    hands = 0
    while hands < 10000:
        deck = shuffleDeck()

        while len(deck) > 78:  # 75% of deck played
            win, draw = playHand(deck)
            winnings += win
            draws += draw
            hands += 1

    print(winnings, draws, hands)
    print("Win %:", float(winnings/hands) * 100)
    print("Loss %:", float((hands-winnings-draws)/hands) * 100)

if __name__ == '__main__':
    blackJack()
