import random

# Определение карты и колоды
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self):
        self.cards = [Card(suit, value) for suit in self.suits for value in self.values]
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

# Определение игрока и дилера (ИИ)
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def calculate_hand_value(self):
        value = 0
        aces = 0
        for card in self.hand:
            if card.value in ['Jack', 'Queen', 'King']:
                value += 10
            elif card.value == 'Ace':
                aces += 1
                value += 11
            else:
                value += int(card.value)

        while value > 21 and aces:
            value -= 10
            aces -= 1

        return value

    def show_hand(self, hide_first_card=False):
        if hide_first_card:
            print(f"{self.name}'s hand: [Hidden], {self.hand[1]}")
        else:
            print(f"{self.name}'s hand: {', '.join(map(str, self.hand))}")

# Определение игры
class BlackJackGame:
    def __init__(self):
        self.deck = Deck()
        self.player = Player("Player")
        self.dealer = Player("Dealer")

    def deal_initial_cards(self):
        for _ in range(2):
            self.player.add_card(self.deck.draw_card())
            self.dealer.add_card(self.deck.draw_card())

    def player_turn(self):
        while True:
            self.player.show_hand()
            choice = input("Do you want to (h)it or (s)tand? ").lower()
            if choice == 'h':
                self.player.add_card(self.deck.draw_card())
                if self.player.calculate_hand_value() > 21:
                    print("You busted!")
                    return False
            elif choice == 's':
                break
        return True

    def dealer_turn(self):
        while self.dealer.calculate_hand_value() < 17:
            self.dealer.add_card(self.deck.draw_card())

    def determine_winner(self):
        player_value = self.player.calculate_hand_value()
        dealer_value = self.dealer.calculate_hand_value()

        print(f"Player's hand: {self.player.hand}, value: {player_value}")
        print(f"Dealer's hand: {self.dealer.hand}, value: {dealer_value}")

        if dealer_value > 21 or player_value > dealer_value:
            print("Player wins!")
        elif player_value == dealer_value:
            print("It's a tie!")
        else:
            print("Dealer wins!")

    def play(self):
        print("Starting a new game of BlackJack!")
        self.deal_initial_cards()
        self.dealer.show_hand(hide_first_card=True)
        if self.player_turn():
            self.dealer_turn()
        self.determine_winner()

if __name__ == "__main__":
    game = BlackJackGame()
    game.play()