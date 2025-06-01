# Pokerbot Project

This repo provides a pokerbot which utilitizes Monte-Carlo Simulation (`player2_monte_carlo`).

## Setup and Installation

**Install Dependencies**: Install the required Python packages using the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

## Running the Bots

To locally run a game between the bots, you can use the test engine script. The game engine is named `test_engine.py` and you have a basic example player in a folder like `player1_ABC`, you can run a match like this:

```bash
python3 test_engine.py
```

## Official Tournament Configuration

Please be aware that the **final tournament will use the following game configuration**: 

*   `NUM_ROUNDS = 1000`
*   `STARTING_STACK = 400`
*   `BIG_BLIND = 2`
*   `SMALL_BLIND = 1`
*   `STARTING_GAME_CLOCK = 10000.0` seconds (per bot for the entire match)

Ensure your bot is optimized and tested to perform well under these specific parameters, especially managing its decision time within the allocated `STARTING_GAME_CLOCK` over 1000 rounds.

## Experimentation and Configuration

This pokerbot, `player2_monte_carlo/player.py`, offers parameters you can tweak for experimentation. When experimenting, always keep the official tournament configuration and especially the `STARTING_GAME_CLOCK` in mind.

### Monte Carlo Iterations (`MONTE_CARLO_ITERS`)

The number of simulations the Monte Carlo bot runs to determine hand strength significantly impacts its performance and, crucially, its decision time.

*   **Location**: Inside `player2_monte_carlo/player.py`, find the variable `MONTE_CARLO_ITERS`.
*   **Experiment**: Try changing this value (e.g., 100, 1000, 5000). 
*   **Time Management**: Observe how changes affect the bot's thinking time per move. A higher iteration count can lead to stronger decisions but consumes more of your `game_clock`. It is vital to find a balance where your bot makes good decisions without exhausting its total allotted time over the 1000 rounds of the tournament.

### Game Time Management (`game_clock`)

*   **Tracking Time**: Your bot's remaining time is available via `game_state.game_clock` within its methods. The initial total game time for the tournament is `10000.0` seconds.
*   **Critical Consideration**: When increasing `MONTE_CARLO_ITERS`, each decision will take longer. Your bot **must** manage its time effectively to avoid exhausting its `game_clock` before all 1000 rounds are complete. Running out of time will result in a loss.
*   **Strategy**: Consider implementing dynamic adjustments to `MONTE_CARLO_ITERS` based on remaining time or average time per round, or thoroughly test a fixed iteration count to ensure it completes within the time limit.

Feel free to explore these settings and other aspects of the bot's logic to understand their impact and potentially improve its performance for the tournament! 