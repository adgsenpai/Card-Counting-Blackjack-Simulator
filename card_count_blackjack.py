import random
import sys

# Card ranks and a standard deck (no suits for simplicity)
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
deck = ranks * 4

# Hi-Lo card counting values
card_count_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

# Shuffle the deck
random.shuffle(deck)

def card_value_for_blackjack(card):
    """Return the blackjack value of a single card."""
    if card in ['J', 'Q', 'K', '10']:
        return 10
    elif card == 'A':
        # Aces handled later (value can be 1 or 11)
        return 11
    else:
        return int(card)

def hand_value(cards):
    """Compute the best value of a blackjack hand."""
    total = 0
    aces = 0
    for c in cards:
        val = card_value_for_blackjack(c)
        if c == 'A':
            aces += 1
        total += val

    # Adjust for aces
    while total > 21 and aces > 0:
        total -= 10  # count an Ace as 1 instead of 11
        aces -= 1
    return total

def ascii_card(card):
    # We'll display the card in a nice ASCII box
    rank_str = card
    width = max(len(rank_str), 2)
    top_bottom = " " + "_" * (width + 2)
    empty_line = "|" + " " * (width + 2) + "|"
    top_line = "|" + rank_str + " " * (width + 2 - len(rank_str)) + "|"
    bottom_line = "|" + " " * (width + 2 - len(rank_str)) + rank_str + "|"
    bottom_border = "‾" * (width + 4)

    card_lines = [
        top_bottom,
        top_line,
        empty_line,
        bottom_line,
        bottom_border
    ]
    return "\n".join(card_lines)

def display_hand(cards, name="Hand"):
    """Display a hand of cards in ASCII."""
    print(f"{name}:")
    # Print cards side by side
    card_lines = [ascii_card(c).split('\n') for c in cards]
    # Each card_lines[i] is a list of lines for that card
    for line_idx in range(len(card_lines[0])):
        line_str = "   ".join(card_lines[c][line_idx] for c in range(len(cards)))
        print(line_str)
    print()

def calculate_true_count(running_count, cards_dealt):
    """Calculate the true count given the running count and cards dealt."""
    # Deck started with 52 cards
    # True count = running_count / number_of_decks_remaining
    # Here we assume just one deck.
    # decks_remaining = (52 - cards_dealt) / 52
    decks_remaining = (52 - cards_dealt) / 52.0 if (52 - cards_dealt) > 0 else 0.1
    true_count = running_count / decks_remaining
    return true_count

def blackjack_round(deck, card_index, running_count):
    """Play a round of blackjack. Returns updated card_index and running_count."""
    player_cards = []
    dealer_cards = []

    # Deal initial hands
    for _ in range(2):
        player_cards.append(deck[card_index])
        running_count += card_count_values[deck[card_index]]
        card_index += 1

        dealer_cards.append(deck[card_index])
        running_count += card_count_values[deck[card_index]]
        card_index += 1

    # Show initial hands (dealer shows both for simplicity)
    display_hand(player_cards, "Player")
    display_hand(dealer_cards, "Dealer")

    # Player turn
    while True:
        p_value = hand_value(player_cards)
        d_value = hand_value(dealer_cards)

        if p_value == 21:
            print("Blackjack! You stand automatically.")
            break

        if p_value > 21:
            print("You busted!")
            break

        # Show advice based on true count and probabilities
        cards_dealt = card_index
        true_count = calculate_true_count(running_count, cards_dealt)
        print(f"Running Count: {running_count}, True Count: {true_count:.2f}")

        # Probability estimation: chance of busting if you hit
        # If player_value = v, you bust if next card > (21 - v)
        # Count how many cards in the deck would bust you
        remaining_deck = deck[card_index:]
        bust_threshold = 22 - p_value
        # Determine bust cards: any card that when added makes you exceed 21
        # For simplicity, just count how many cards have a value >= bust_threshold
        # Note: This is rough since Aces can be flexible, but let's simplify.
        bust_cards = 0
        for c in remaining_deck:
            val = card_value_for_blackjack(c)
            # Adjust aces logic roughly: If bust_threshold <= 11 and card is 'A', it can be 11 or 1, might not always bust.
            # We'll just assume 11-value A is always bad if val >= bust_threshold.
            if val >= bust_threshold:
                bust_cards += 1

        if len(remaining_deck) > 0:
            bust_probability = (bust_cards / len(remaining_deck)) * 100
        else:
            bust_probability = 0

        # Simple advice:
        # If true_count > 2, lean towards standing if you're above 15.
        # If true_count < 0, more likely to hit if below 17.
        # Otherwise basic strategy: hit if < 17, stand if >= 17
        advice = "Stand" if p_value >= 17 else "Hit"
        if true_count > 2 and p_value >= 15:
            advice = "Stand (High Count)"
        elif true_count < 0 and p_value < 17:
            advice = "Hit (Low Count)"

        print(f"Player Total: {p_value}, Dealer Showing: {d_value}")
        print(f"Estimated Bust Probability on Hit: {bust_probability:.1f}%")
        print(f"Recommended Action: {advice}")

        action = input("(H)it, (S)tand: ").strip().lower()
        if action == 'h':
            # Hit
            player_cards.append(deck[card_index])
            running_count += card_count_values[deck[card_index]]
            card_index += 1
            display_hand(player_cards, "Player")
        elif action == 's':
            # Stand
            break
        else:
            print("Invalid action, please type H or S.")

    # Dealer turn if player hasn't busted
    p_value = hand_value(player_cards)
    if p_value <= 21:
        # Dealer hits until >= 17
        while hand_value(dealer_cards) < 17:
            dealer_cards.append(deck[card_index])
            running_count += card_count_values[deck[card_index]]
            card_index += 1
        display_hand(dealer_cards, "Dealer")

        d_value = hand_value(dealer_cards)
        print(f"Player: {p_value}, Dealer: {d_value}")
        if d_value > 21:
            print("Dealer busts, you win!")
        elif d_value > p_value:
            print("Dealer wins!")
        elif d_value < p_value:
            print("You win!")
        else:
            print("Push (tie)!")
    else:
        print("Dealer does not need to play since you busted.")

    return card_index, running_count

def main():
    running_count = 0
    card_index = 0
    total_cards = len(deck)

    print("Welcome to the Card Counting & Blackjack Simulator!")
    print("Commands:")
    print("- Press Enter: Draw next card for counting practice.")
    print("- Type 'count': Guess your current running count.")
    print("- Type 'play': Start a blackjack round.")
    print("- Type 'quit': Exit the simulator.")
    print("--------------------------------------------------------")

    while card_index < total_cards:
        user_input = input("Press Enter (draw), 'count', 'play', or 'quit': ").strip().lower()

        if user_input == 'quit':
            print("Thank you for playing! Goodbye.")
            sys.exit(0)

        elif user_input == 'count':
            guess = input("Enter your current count guess: ")
            try:
                guess = int(guess)
                if guess == running_count:
                    print("Correct! Your guessed count matches the actual running count.")
                else:
                    print(f"Your guess: {guess}. Actual count: {running_count}. Keep practicing!")
            except ValueError:
                print("Please enter a valid integer for your guess.")
            continue

        elif user_input == 'play':
            # Start a blackjack round if there are enough cards left
            cards_left = total_cards - card_index
            if cards_left < 10:
                print("Not enough cards left to play a new blackjack hand. Try again later.")
                continue
            card_index, running_count = blackjack_round(deck, card_index, running_count)
            continue

        elif user_input == '':
            # Draw the next card (counting practice)
            if card_index >= total_cards:
                break
            card = deck[card_index]
            print("\nDealing card:")
            print(ascii_card(card))
            # Update running count
            running_count += card_count_values[card]
            card_index += 1
        else:
            print("Invalid command. Use Enter, 'count', 'play', or 'quit'.")
            continue

    print("All cards have been dealt.")
    # Final guess
    final_guess = input("All cards are done. Enter your final count guess: ").strip()
    try:
        final_guess = int(final_guess)
        if final_guess == running_count:
            print("Perfect! You got the final count correct!")
        else:
            print(f"Final guess: {final_guess}. Actual final count: {running_count}. Better luck next time!")
    except ValueError:
        print(f"Invalid guess. The actual final count was {running_count}.")

if __name__ == "__main__":
    main()
