import random
from collections import Counter
from src.game_enums import NO_MATCH, EXACT, PARTIAL, WON, LOST, IN_PROGRESS
from src.color import Color
 
MAX_ATTEMPTS = 20
MAX_COLORS = 6
 
def guess(user_provided_colors, selected_colors):
    def match_for_position(position):
        candidate_color = user_provided_colors[position]
        if candidate_color == selected_colors[position]:
            return EXACT
 
        if candidate_color in user_provided_colors[:position]:
            return NO_MATCH
 
        index = selected_colors.index(candidate_color) if candidate_color in selected_colors else -1
        return PARTIAL if index > -1 and selected_colors[index] != user_provided_colors[index] else NO_MATCH
 
    return {**{EXACT: 0, PARTIAL: 0, NO_MATCH: 0}, **Counter(map(match_for_position, range(MAX_COLORS)))}
 
def play(selected_colors, user_provided_colors, number_of_attempts=1):
    if number_of_attempts > MAX_ATTEMPTS:
        raise ValueError("Exceeded maximum attempts")
 
    result = guess(user_provided_colors, selected_colors)
    attempts_made = number_of_attempts + 1
 
    status = IN_PROGRESS
 
    if result[EXACT] == MAX_COLORS:
        status = WON
    elif attempts_made > MAX_ATTEMPTS:
        status = LOST
 
    return result, attempts_made, status
 
def select_colors(seed):
    random.seed(seed)
    return random.sample(list(Color), MAX_COLORS)
