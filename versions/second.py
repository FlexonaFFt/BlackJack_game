import telebot
import random

API_TOKEN = '7203910055:AAGNQcSiHfNESMQdLUBXcED9enj7DvSPIis'

bot = telebot.TeleBot(API_TOKEN)

# Карты и их значения
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 2, 'Q': 3, 'K': 4, 'A': 11}

# Состояния игры
user_games = {}

class BlackjackGame:
    def __init__(self):
        self.player_hand = []
        self.dealer_hand = []
        self.player_score = 0
        self.dealer_score = 0
        self.game_over = False

    def deal_initial_cards(self):
        self.player_hand = [self.draw_card(), self.draw_card()]
        self.dealer_hand = [self.draw_card(), self.draw_card()]
        self.update_scores()

    def draw_card(self):
        return random.choice(cards)

    def update_scores(self):
        self.player_score = self.calculate_score(self.player_hand)
        self.dealer_score = self.calculate_score(self.dealer_hand)

    def calculate_score(self, hand):
        score = sum(card_values[card] for card in hand)
        # Adjust for Aces
        num_aces = hand.count('A')
        while score > 21 and num_aces:
            score -= 10
            num_aces -= 1
        return score

    def player_hit(self):
        self.player_hand.append(self.draw_card())
        self.update_scores()

    def dealer_play(self):
        while self.dealer_score < 17:
            self.dealer_hand.append(self.draw_card())
            self.update_scores()

@bot.message_handler(commands=['start'])
def start_game(message):
    user_id = message.from_user.id
    game = BlackjackGame()
    game.deal_initial_cards()
    user_games[user_id] = game
    bot.send_message(message.chat.id, f"{message.from_user.first_name}, ваши карты: {game.player_hand} (сумма: {game.player_score})\nКарты дилера: [{game.dealer_hand[0]}, ?]")
    bot.send_message(message.chat.id, f"{message.from_user.first_name}, напишите /hit чтобы взять ещё карту или /stand чтобы закончить игру.")

@bot.message_handler(commands=['hit'])
def hit(message):
    user_id = message.from_user.id
    game = user_games.get(user_id)
    if not game:
        bot.send_message(message.chat.id, f"{message.from_user.first_name}, игра не найдена. Начните новую игру с /start.")
        return

    game.player_hit()
    if game.player_score > 21:
        bot.send_message(message.chat.id, f"{message.from_user.first_name}, ваши карты: {game.player_hand} (сумма: {game.player_score})\nВы проиграли!")
        user_games.pop(user_id)
    else:
        bot.send_message(message.chat.id, f"{message.from_user.first_name}, ваши карты: {game.player_hand} (сумма: {game.player_score})\nНапишите /hit чтобы взять ещё карту или /stand чтобы закончить игру.")

@bot.message_handler(commands=['stand'])
def stand(message):
    user_id = message.from_user.id
    game = user_games.get(user_id)
    if not game:
        bot.send_message(message.chat.id, f"{message.from_user.first_name}, игра не найдена. Начните новую игру с /start.")
        return

    game.dealer_play()
    if game.dealer_score > 21 or game.player_score > game.dealer_score:
        result = "Вы выиграли!"
    elif game.player_score < game.dealer_score:
        result = "Вы проиграли!"
    else:
        result = "Ничья!"

    bot.send_message(message.chat.id, f"{message.from_user.first_name}, ваши карты: {game.player_hand} (сумма: {game.player_score})\nКарты дилера: {game.dealer_hand} (сумма: {game.dealer_score})\n{result}")
    user_games.pop(user_id)

bot.polling()
