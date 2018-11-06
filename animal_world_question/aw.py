#!/usr/bin/python
# -*- coding: utf8 -*-
from random import randrange

class Player:
    def __init__(self, init_cards_count):
        self.stars = 3
        # stone=0, cicsser=1, cloth=2
        self.cards = [0,0,0,0,1,1,1,1,2,2,2,2]

    def play_a_card(self):
        random_index = randrange(len(self.cards))
        played_card = self.cards[random_index]
        del self.cards[random_index]
        return played_card

    def add_star(self):
        self.stars = self.stars + 1

    def lose_star(self):
        self.stars = self.stars - 1

    def is_alive(self):
        if self.stars <= 0:
            return False
        else:
            return True

    def has_card(self):
        if self.cards:
            return True
        else:
            return False

def test_result(card1, card2):
    d = card1 - card2
    if d == 0: return 0
    if d == -1 or d == 2: return 1
    if d == 1 or d == -2: return 2

def match(player1, player2):
    player1_card = player1.play_a_card()
    player2_card = player2.play_a_card()
    #print "player 1 played card %d, player2 played card %d" % (player1_card, player2_card)
    result = test_result(player1_card, player2_card)
    if result == 1:
        player1.add_star()
        player2.lose_star()
    if result == 2:
        player1.lose_star()
        player2.add_star()

def game(player1, player2):
    turns = 0
    while player1.is_alive() and player1.has_card() \
            and player2.is_alive() and player2.has_card():
        turns = turns + 1
        match(player1, player2)
    #print "this game has %d turns" % turns
    game_turns_hash[turns] =  game_turns_hash[turns] + 1
    if player1.is_alive() and player2.is_alive():
        return (turns, 1)
    else:
        return (turns, 0)

total_turns = 0
total_both_alive = 0
total_games = 100000
game_turns_hash = {}
for i in range(3, 13):
    game_turns_hash[i] = 0
i = 0
while i< total_games:
    p1 = Player(12)
    p2 = Player(12)
    game_result = game(p1,p2)
    total_turns = total_turns + game_result[0]
    total_both_alive = total_both_alive + game_result[1]
    i = i+ 1
print game_turns_hash
print u"平均游戏轮数：%f " % (total_turns / float(total_games))
print u"两人都幸存的概率：%f " % (total_both_alive / float(total_games))
