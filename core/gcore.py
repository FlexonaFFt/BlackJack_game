import random

# Определяем классы карты и колоды
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

    def __init__(self):
        self.deck = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

# Определяем класс руки
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += Deck.values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
        self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

# Функция для отображения карт
def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <hidden card>")
    print('', dealer.cards[1])  
    print("\nPlayer's Hand:", *player.cards, sep='\n ')

def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)

# Основная логика игры
def blackjack():
    # Создаем и перемешиваем колоду
    deck = Deck()

    # Раздаем карты игроку и дилеру
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Показываем карты (одна карта дилера скрыта)
    show_some(player_hand, dealer_hand)

    while True:  
        action = input("\nWould you like to Hit or Stand? Enter 'h' or 's': ")

        if action[0].lower() == 'h':
            player_hand.add_card(deck.deal())
            show_some(player_hand, dealer_hand)

            if player_hand.value > 21:
                print("\nPlayer busts!")
                break
        else:
            while dealer_hand.value < 17:
                dealer_hand.add_card(deck.deal())
            
            show_all(player_hand, dealer_hand)

            if dealer_hand.value > 21:
                print("\nDealer busts!")
            elif dealer_hand.value > player_hand.value:
                print("\nDealer wins!")
            elif dealer_hand.value < player_hand.value:
                print("\nPlayer wins!")
            else:
                print("\nIt's a tie!")

            break

def player_busts(player, dealer):
    print("\nPlayer busts! Dealer wins.")

def player_wins(player, dealer):
    print("\nPlayer wins!")

def dealer_busts(player, dealer):
    print("\nDealer busts! Player wins!")

def dealer_wins(player, dealer):
    print("\nDealer wins!")

def push(player, dealer):
    print("\nDealer and Player tie! It's a push.")

def play_blackjack():
    while True:
        # Создаем и перемешиваем колоду
        deck = Deck()

        # Раздаем карты игроку и дилеру
        player_hand = Hand()
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())

        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

        # Показываем карты (одна карта дилера скрыта)
        show_some(player_hand, dealer_hand)

        while True:
            action = input("\nWould you like to Hit or Stand? Enter 'h' or 's': ")

            if action[0].lower() == 'h':
                player_hand.add_card(deck.deal())
                show_some(player_hand, dealer_hand)

                if player_hand.value > 21:
                    player_busts(player_hand, dealer_hand)
                    break
            else:
                while dealer_hand.value < 17:
                    dealer_hand.add_card(deck.deal())

                show_all(player_hand, dealer_hand)

                if dealer_hand.value > 21:
                    dealer_busts(player_hand, dealer_hand)
                elif dealer_hand.value > player_hand.value:
                    dealer_wins(player_hand, dealer_hand)
                elif dealer_hand.value < player_hand.value:
                    player_wins(player_hand, dealer_hand)
                else:
                    push(player_hand, dealer_hand)

                break

        new_game = input("\nWould you like to play again? Enter 'y' or 'n': ")
        if new_game[0].lower() == 'n':
            print("Thanks for playing!")
            break

play_blackjack()

blackjack()