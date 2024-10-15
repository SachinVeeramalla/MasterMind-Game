import unittest, random
from src.master_mind import guess, play, select_colors, MAX_COLORS
from src.game_enums import NO_MATCH, EXACT, PARTIAL, WON, LOST, IN_PROGRESS
from src.color import Color
  
class MasterMindTests(unittest.TestCase):
    def test_canary(self):
        self.assertTrue(True)
        
    def test_all_colors_mismatch(self):
        selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.PURPLE, Color.ORANGE]
        user_provided_colors = [Color.CYAN, Color.CYAN, Color.CYAN, Color.CYAN, Color.CYAN, Color.CYAN]
        
        result = guess(user_provided_colors, selected_colors)
        
        self.assertEqual(result[NO_MATCH], 6)
    
    def test_all_colors_match(self):
        selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.PURPLE, Color.ORANGE]
        user_provided_colors = selected_colors
        
        result = guess(user_provided_colors, selected_colors)
        
        self.assertEqual(result[EXACT], 6)
    
    def test_all_colors_match_out_of_position(self):
        selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.PURPLE, Color.ORANGE]
        user_provided_colors = [Color.ORANGE, Color.PURPLE, Color.YELLOW, Color.GREEN, Color.BLUE, Color.RED]
        
        result = guess(user_provided_colors, selected_colors)
        
        self.assertEqual(result[PARTIAL], 6)
    
    def test_first_four_colors_match_in_position(self):
        selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.PURPLE, Color.ORANGE]
        user_provided_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.CYAN, Color.MAGENTA]
        
        result = guess(user_provided_colors, selected_colors)
        
        self.assertEqual(result, {EXACT: 4, PARTIAL: 0, NO_MATCH: 2})
 
    def test_last_four_colors_match_in_position(self):
        selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.PURPLE, Color.ORANGE]
        user_provided_colors = [Color.CYAN, Color.MAGENTA, Color.GREEN, Color.YELLOW, Color.PURPLE, Color.ORANGE]
        
        result = guess(user_provided_colors, selected_colors)
        
        self.assertEqual(result, {EXACT: 4, PARTIAL: 0, NO_MATCH: 2})
    
    def test_first_three_match_in_position_last_three_out_of_position(self):
        selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.PURPLE, Color.ORANGE]
        user_provided_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.ORANGE, Color.YELLOW, Color.PURPLE]
        
        result = guess(user_provided_colors, selected_colors)
        
        self.assertEqual(result, {EXACT: 3, PARTIAL: 3, NO_MATCH: 0})
 
    def test_first_and_third_color_mismatch_second_in_position_others_out_of_position(self):
        selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.PURPLE, Color.ORANGE]
        user_provided_colors = [Color.ORANGE, Color.BLUE, Color.MAGENTA, Color.PURPLE, Color.YELLOW, Color.CYAN]
        
        result = guess(user_provided_colors, selected_colors)
        
        self.assertEqual(result, {EXACT: 1, PARTIAL: 3, NO_MATCH: 2})
 
    def test_guess_with_first_color_repeated_five_times(self):
        selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.PURPLE, Color.ORANGE]
        user_provided_colors = [Color.RED, Color.RED, Color.RED, Color.RED, Color.RED, Color.CYAN]
        
        result = guess(user_provided_colors, selected_colors)
        
        self.assertEqual(result, {EXACT: 1, PARTIAL: 0, NO_MATCH: 5})
 
    def test_guess_with_last_color_repeated(self):
        selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.PURPLE, Color.ORANGE]
        user_provided_colors = [Color.ORANGE, Color.ORANGE, Color.ORANGE, Color.ORANGE, Color.ORANGE, Color.ORANGE]
        
        result = guess(user_provided_colors, selected_colors)
        
        self.assertEqual(result, {EXACT: 1, PARTIAL: 0, NO_MATCH: 5})
 
    def test_guess_first_position_with_second_color_rest_repeated_first_color(self):
        selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.PURPLE, Color.ORANGE]
        user_provided_colors = [Color.BLUE, Color.RED, Color.RED, Color.RED, Color.RED, Color.RED]
        
        result = guess(user_provided_colors, selected_colors)
        
        self.assertEqual(result, {EXACT: 0, PARTIAL: 2, NO_MATCH: 4})
 
    def test_guess_first_position_no_match_rest_repeated_first_color(self):
        selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.PURPLE, Color.ORANGE]
        user_provided_colors = [Color.MAGENTA, Color.RED, Color.RED, Color.RED, Color.RED, Color.RED]
        
        result = guess(user_provided_colors, selected_colors)
        
        self.assertEqual(result, {EXACT: 0, PARTIAL: 1, NO_MATCH: 5})
    
    def test_play_first_attempt_exact_match(self):
        selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.PURPLE, Color.ORANGE]
        user_provided_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.PURPLE, Color.ORANGE]
 
        result, attempts, status = play(selected_colors, user_provided_colors, 1)
 
        self.assertEqual(result, {EXACT: 6, PARTIAL: 0, NO_MATCH: 0})
        self.assertEqual(attempts, 2)
        self.assertEqual(status, WON)
    
    def test_play_first_attempt_no_match(self):
        selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.PURPLE, Color.ORANGE]
        user_provided_colors = [Color.CYAN, Color.CYAN, Color.CYAN, Color.CYAN, Color.CYAN, Color.CYAN]
 
        result, attempts, status = play(selected_colors, user_provided_colors, 1)
 
        self.assertEqual(result, {EXACT: 0, PARTIAL: 0, NO_MATCH: 6})
        self.assertEqual(attempts, 2)
        self.assertEqual(status, IN_PROGRESS)
        
    def test_play_first_attempt_some_exact_and_some_non_exact(self):
        selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.PURPLE, Color.ORANGE]
        user_provided_colors = [Color.RED, Color.PURPLE, Color.GREEN, Color.ORANGE, Color.YELLOW, Color.BLUE]
 
        result, attempts, status = play(selected_colors, user_provided_colors, 1)
 
        self.assertEqual(result, {EXACT: 2, PARTIAL: 4, NO_MATCH: 0})
        self.assertEqual(attempts, 2)
        self.assertEqual(status, IN_PROGRESS)
    
    def test_play_second_attempt_exact_match(self):
        selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.PURPLE, Color.ORANGE]
        user_provided_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.PURPLE, Color.ORANGE]
 
        result, attempts, status = play(selected_colors, user_provided_colors, 2)
 
        self.assertEqual(result, {EXACT: 6, PARTIAL: 0, NO_MATCH: 0})
        self.assertEqual(attempts, 3)
        self.assertEqual(status, WON)
    
    def test_play_second_attempt_no_match(self):
        selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.PURPLE, Color.ORANGE]
        user_provided_colors = [Color.CYAN, Color.CYAN, Color.CYAN, Color.CYAN, Color.CYAN, Color.CYAN]
 
        result, attempts, status = play(selected_colors, user_provided_colors, 2)
 
        self.assertEqual(result, {EXACT: 0, PARTIAL: 0, NO_MATCH: 6})
        self.assertEqual(attempts, 3)
        self.assertEqual(status, IN_PROGRESS)
        
    def test_play_twentieth_attempt_exact_match(self):
        selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.PURPLE, Color.ORANGE]
        user_provided_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.PURPLE, Color.ORANGE]
 
        result, attempts, status = play(selected_colors, user_provided_colors, 20)
 
        self.assertEqual(result, {EXACT: 6, PARTIAL: 0, NO_MATCH: 0})
        self.assertEqual(attempts, 21)
        self.assertEqual(status, WON)
 
    def test_play_twentieth_attempt_no_match(self):
        selected_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.PURPLE, Color.ORANGE]
        user_provided_colors = [Color.CYAN, Color.CYAN, Color.CYAN, Color.CYAN, Color.CYAN, Color.CYAN]
 
        result, attempts, status = play(selected_colors, user_provided_colors, 20)
 
        self.assertEqual(result, {EXACT: 0, PARTIAL: 0, NO_MATCH: 6})
        self.assertEqual(attempts, 21)
        self.assertEqual(status, LOST)
 
    def test_play_twenty_first_attempt_with_exact_match(self):
        selected_colors = [Color.RED, Color.BLUE, Color.YELLOW, Color.GREEN, Color.GOLD, Color.CYAN]
        user_provided_colors = [Color.RED, Color.BLUE, Color.YELLOW, Color.GREEN, Color.GOLD, Color.CYAN]
 
        self.assertRaisesRegex(ValueError, "Exceeded maximum attempts", play, selected_colors, user_provided_colors, 21)
 
    def test_play_twenty_first_attempt_with_no_match(self):
        selected_colors = [Color.RED, Color.BLUE, Color.YELLOW, Color.GREEN, Color.GOLD, Color.CYAN]
        user_provided_colors = [Color.CYAN, Color.CYAN, Color.CYAN, Color.CYAN, Color.CYAN, Color.CYAN]
        
        self.assertRaisesRegex(ValueError, "Exceeded maximum attempts", play, selected_colors, user_provided_colors, 21)
                
    def test_randomized_selected_colors_given(self):
        
        selected_colors = select_colors(seed=42) 
        self.assertEqual(len(selected_colors), MAX_COLORS)  

        self.assertTrue(set(selected_colors).issubset(Color)) 

    def test_randomized_selected_colors_different_when_called_twice(self):
        selection_1 = select_colors(seed=42)
        selection_2 = select_colors(seed=43)
        
        self.assertNotEqual(selection_1, selection_2)

if __name__ == '__main__':
    unittest.main()
