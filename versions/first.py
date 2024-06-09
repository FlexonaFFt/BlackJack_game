import telebot
import random

API_TOKEN = '7203910055:AAGNQcSiHfNESMQdLUBXcED9enj7DvSPIis'
BOT_USERNAME = 'black_jack_cat_bot'

bot = telebot.TeleBot(API_TOKEN)

# Карты и их значения
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 2, 'Q': 3, 'K': 4, 'A': 11}

# Состояния игры
games = {}

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

def is_command_for_bot(message):
    if message.chat.type in ['group', 'supergroup']:
        if message.text.startswith('/'):
            command = message.text.split()[0][1:]
            if '@' in command:
                command, username = command.split('@')
                if username.lower() == BOT_USERNAME.lower():
                    return command
    return None

@bot.message_handler(func=lambda message: message.chat.type == 'private' and message.text.startswith('/'))
@bot.message_handler(func=lambda message: is_command_for_bot(message))
def handle_command(message):
    command = message.text.split()[0][1:].split('@')[0]
    if command == 'start':
        start_game(message)
    elif command == 'hit':
        hit(message)
    elif command == 'stand':
        stand(message)

def start_game(message):
    chat_id = message.chat.id
    game = BlackjackGame()
    game.deal_initial_cards()
    games[chat_id] = game
    bot.send_message(chat_id, f"Ваши карты: {game.player_hand} (сумма: {game.player_score})\nКарты дилера: [{game.dealer_hand[0]}, ?]")
    bot.send_message(chat_id, "Напишите /hit чтобы взять ещё карту или /stand чтобы закончить игру.")

def hit(message):
    chat_id = message.chat.id
    game = games.get(chat_id)
    if not game:
        bot.send_message(chat_id, "Игра не найдена. Начните новую игру с /start.")
        return

    game.player_hit()
    if game.player_score > 21:
        bot.send_message(chat_id, f"Ваши карты: {game.player_hand} (сумма: {game.player_score})\nВы проиграли!")
        games.pop(chat_id)
    else:
        bot.send_message(chat_id, f"Ваши карты: {game.player_hand} (сумма: {game.player_score})\nНапишите /hit чтобы взять ещё карту или /stand чтобы закончить игру.")

def stand(message):
    chat_id = message.chat.id
    game = games.get(chat_id)
    if not game:
        bot.send_message(chat_id, "Игра не найдена. Начните новую игру с /start.")
        return

    game.dealer_play()
    if game.dealer_score > 21 or game.player_score > game.dealer_score:
        result = "Вы выиграли!"
    elif game.player_score < game.dealer_score:
        result = "Вы проиграли!"
    else:
        result = "Ничья!"

    bot.send_message(chat_id, f"Ваши карты: {game.player_hand} (сумма: {game.player_score})\nКарты дилера: {game.dealer_hand} (сумма: {game.dealer_score})\n{result}")
    games.pop(chat_id)

bot.polling()