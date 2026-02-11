import random
from datetime import datetime, timedelta

from tqdm import tqdm


WORD_LENGTH = 5
WINNING_WORD = None
WINNING_WORD_LETTER_COUNT = None
MAX_GUESSES = 6
DICTIONARY = []
with open('odm.txt', "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        words = line.split(",")

        for word in words:
            word = word.strip().lower()
            if word and len(word) == WORD_LENGTH and ' ' not in word and '-' not in word:
                DICTIONARY.append(word)
DICTIONARY = list(set(DICTIONARY))

def count_lettes_in_word(word):
    letter_count = {}
    for letter in word:
        if letter not in letter_count.keys():
            letter_count[letter] = 1
        else:
            letter_count[letter] +=1
    return letter_count

DICTIONARY_FOR_GUESSING = []
for word in DICTIONARY:
    DICTIONARY_FOR_GUESSING.append({
        'word': word,
        'letters':count_lettes_in_word(word),
        'chars': tuple(word)
    })
print("Słownik przygotowany! Słów:", len(DICTIONARY))
def __score_word(word, options):
    score = 0
    word = set(tuple(word))
    for letter in word:
        for x_word in options:
            score += x_word.count(letter)
    return score
def getBestGuess(options):
    options = list([(__score_word(word, options), word) for word in options])
    options.sort(key= lambda x: x[0], reverse=True)
    return options
def filter_list_classic(options_left, result, guessed_word):
    letter_count = {}
    max_letters = []
    for index in range(0, WORD_LENGTH):
        letter = guessed_word[index]
        if letter not in letter_count.keys():
            letter_count[letter] = 0
        match result[index]:
            case '_':
                max_letters.append(letter)
            case 'x':
                letter_count[letter] += 1
                options_left = [word for word in options_left
                                if word[index] == letter]
            case '?':
                options_left = [word for word in options_left
                                if word[index] != letter]
                letter_count[letter] += 1
    for letter in max_letters:
        options_left = [word for word in options_left
                        if word.count(letter) == letter_count[letter]]
    for letter in letter_count.keys():
        options_left = [word for word in options_left
                        if word.count(letter) >= letter_count[letter]]
    return options_left
def roll_word():
    global WINNING_WORD, WINNING_WORD_LETTER_COUNT
    WINNING_WORD = random.choice(DICTIONARY)
    WINNING_WORD_LETTER_COUNT = {}
    for letter in WINNING_WORD:
        WINNING_WORD_LETTER_COUNT[letter] = WINNING_WORD.count(letter)
def robot_play():
    options_left = DICTIONARY.copy()
    guess_number = 1

    while guess_number <= MAX_GUESSES:
        guessed_word = random.choice(options_left)
        print(f"Próba {guess_number}: {guessed_word}")
        try:
            result = check_word(guessed_word)
            options_left = filter_list_classic(options_left, result, guessed_word)
        except ValueError as e:
            print(e)
def robot_assist():
    options_left = DICTIONARY.copy()
    user_still_playing = True
    guess_number = 0
    print("Asysta w zgadywaniu! By zakończyć, wpisz #")
    options_scored = None
    while user_still_playing:
        best_guess_try = 0
        if guess_number == 0:
            guessed_word = random.choice(options_left)
        else:
            options_scored = getBestGuess(options_left)
            print(options_scored[:5])
            guessed_word = options_scored[best_guess_try][1]
        print(f"Próba {guess_number}: {guessed_word}")
        result = input("Wynik literowy: ").lower()
        user_info = "Nieprawidłowy input. spróbuj ponownie: "
        while not (len(result) == 5 or result in ('#') or (result=='n' and not options_scored)):
            if 'n' in result and options_scored:
                user_info = "Wynik literowy: "
                best_guess_try += 1
                guessed_word = options_scored[best_guess_try][1]
                print(f"Próba {guess_number}: {guessed_word}")
            result = input(user_info).lower()
            user_info = "Nieprawidłowy input. spróbuj ponownie: "
        if '#' in result:
            user_still_playing = False
            continue
        if 'n' in result:
            continue
        result = [letter for letter in result]
        options_left = filter_list_classic(options_left, result, guessed_word)
        print("Pozostało opcji", len(options_left))
        if len(options_left) <= 10:
            print(options_left)
        guess_number += 1
def check_word(word):
    '''

    :param word: String
    :return:
    :raises:
        ValueError - when word is not a correct word (not in dictionary or bad length)
    '''
    if len(word) != WORD_LENGTH:
        raise ValueError("Niepoprawna długość hasła")
    if word not in DICTIONARY:
        raise ValueError("Brak hasła w słowniku")
    if word == WINNING_WORD:
        return True
    else:
        ret = []
        guess_letter_count = {}
        for letter_index in range(0,WORD_LENGTH):
            current_letter = word[letter_index]
            #Make dict for letter
            if current_letter not in guess_letter_count.keys():
                guess_letter_count[current_letter] = 0

            if current_letter == WINNING_WORD[letter_index]:
                ret.append('x')
                # Add count to guessed correctly
                guess_letter_count[current_letter] += 1
            else:
                ret.append(None)

        # Calculate number of apperances left
        for letter in guess_letter_count:
            if letter in WINNING_WORD_LETTER_COUNT.keys():
                guess_letter_count[letter] = WINNING_WORD_LETTER_COUNT[letter] - guess_letter_count[letter]

        for index in range(0,WORD_LENGTH):
            if ret[index] is None:
                letter = word[index]
                if guess_letter_count[letter] > 0:
                    ret[index] = '?'
                    guess_letter_count[letter] -= 1
                else:
                    ret[index] = "_"


    return ret
def play():
    guess_number = 1

    while guess_number <= MAX_GUESSES:
        guessed_word = input(f'podejście numer {guess_number}: ').lower()
        try:
            result = check_word(guessed_word)
            if result == True:
                print("GRATULACJE!!!")
                guess_number = MAX_GUESSES
            else:
                print(result)
            guess_number +=1
        except ValueError as e:
            print(e)

    print("Prawidłowe słowo:", WINNING_WORD)

def robot_play2():
    options_left = DICTIONARY_FOR_GUESSING.copy()
    guess_number = 1

    while guess_number <= MAX_GUESSES:
        guessed_word = random.choice(options_left)
        try:
            result = check_word(guessed_word['word'])
            if result == True:
                guess_number = MAX_GUESSES
            else:
                letter_count = {}
                for index in range(0, WORD_LENGTH):
                    letter = guessed_word['chars'][index]
                    if letter not in letter_count.keys():
                        letter_count[letter] = 0
                    match result[index]:
                        case '_':
                            pass
                        case 'x':
                            letter_count[letter] += 1
                            options_left = [word for word in options_left if word['chars'][index] == letter]
                        case '?':
                            letter_count[letter] += 1

                for letter in letter_count.keys():
                    options_left = [
                        word for word in options_left
                        if word['letters'].get(letter, 0) >= letter_count[letter]
                    ]
            guess_number +=1
        except ValueError as e:
            print(e)
if __name__ == '__main__':
    while True:
        robot_assist()
# if __name__ == '__main__':
#     times = []
#     times2 = []
#     ti_score = 0
#     ti_better_times = []
#     tz_score = 0
#     tz_better_times = []
#
#     for i in range(0, 10):
#         roll_word()
#         print(f"[{i}] Prawidłowe słowo:", WINNING_WORD)
#         time_start = datetime.now()
#         robot_play()
#         times.append(datetime.now()-time_start)
#         ti = datetime.now()-time_start
#         print("Zakończone -> 1", ti)
#
#         time_start = datetime.now()
#         robot_play2()
#         times2.append(datetime.now()-time_start)
#         tz = datetime.now()-time_start
#         print("Zakończone -> 2", tz)
#
#         if ti>tz:
#             tz_score +=1
#             tz_better_times.append(ti-tz)
#         elif tz>ti:
#             ti_score +=1
#             ti_better_times.append(tz - ti)
#
#
#     print("\n\nRozwiązanie zoptymalizowane(?): ")
#     print("Średnio 10:", sum(times2, timedelta(0))*10 / len(times2))
#
#     print("\n\nRozwiązanie intuicyjne: ")
#     print("Średnio 10:", sum(times, timedelta(0))*10 / len(times))
#
#     print("intuicyjne/zoptymalizowane")
#     print(f"Średnio: {sum(times, timedelta(0))*10 / len(times)}/{sum(times2, timedelta(0))*10 / len(times2)}")
#     print(f"Częściej szybszy: {ti_score}/{tz_score}")
#     print(f'Średnio szybciej o {sum(ti_better_times, timedelta(0)) / len(ti_better_times)}/{sum(tz_better_times, timedelta(0))*10 / len(tz_better_times)}')