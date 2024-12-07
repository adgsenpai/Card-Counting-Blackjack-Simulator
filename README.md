# Card Counting & Blackjack Simulator

This is a terminal-based card counting and simplified blackjack simulation. It allows you to practice card counting, estimate probabilities, and make informed decisions to "hit" or "stand" based on the running count and true count of the deck.

## Features

1. **Card Counting Practice:**  
   - Press **Enter** to reveal cards one by one from a shuffled deck.
   - Track the running count mentally.
   - Guess the current running count at any time using the `'count'` command to check your accuracy.

2. **Blackjack Gameplay:**  
   - Type `'play'` to start a simplified blackjack round.
   - The dealer deals two cards to you and two to themselves.
   - You can decide to hit or stand after seeing your total and the dealer's showing card.
   - The simulator provides an estimated probability of busting if you hit.
   - The simulator also calculates and shows the running and true counts, offering advice based on the true count.
   - Follow the recommended action to practice applying card counting strategies in a blackjack setting.

3. **Card Visualization:**  
   - Each card is displayed as a small ASCII art box to help you visualize the dealing process.

## How to Run

1. **Prerequisites:**
   - Python 3.x installed on your machine.

2. **Running the Program:**
   - Save the provided code into a file, for example, `card_count_blackjack.py`.
   - Run the program in a terminal:
     ```bash
     python card_count_blackjack.py
     ```

3. **Interacting with the Program:**
   - **Enter**: Reveal the next card to practice counting.
   - **'count'**: Enter your guess of the current running count.
   - **'play'**: Start a blackjack round and follow the prompts.
   - **'quit'**: Exit the program.

## Understanding the Concepts

- **Running Count (RC):**  
  Each card dealt adjusts the RC by a certain value (Hi-Lo system):
  - 2–6: +1  
  - 7–9: 0  
  - 10, J, Q, K, A: -1

  A positive RC suggests there are relatively more high-value cards left, which is typically favorable to the player. A negative RC suggests the opposite.

- **True Count (TC):**  
  The TC refines the RC by adjusting for how many cards remain in the deck.  
  \[
  \text{TC} = \frac{\text{RC}}{\text{decks remaining}}
  \]

  If the TC is high, it usually indicates better odds for the player.

- **Estimated Bust Probability:**  
  Before hitting, the program estimates how likely it is that the next card will push the player's total over 21. This is a rough estimate, helping you decide whether to hit or stand.

## Notes

- This is a simplified model:
  - It does not implement all blackjack rules (e.g., splitting, doubling down).
  - It assumes a single deck and a simplified dealing method.
  - Probability and strategy calculations are approximations and should be seen as practice tools, not perfect predictions.

- Over time, practicing with the running and true counts can help you develop a sense of when hitting or standing is more advantageous, reflecting real card counting techniques used at blackjack tables.

## Disclaimer

Card counting and blackjack strategy can be complex. This simulator is for educational and practice purposes only. It does not guarantee success in real-life casino settings and is intended to help you understand the basic principles of card counting and decision-making in a controlled environment.
