import numpy as np

# 1. Players
PLAYERS = ["Iran", "China", "Russia", "USA", "Israel"]

# 2. Types
TYPES = {
    "Iran": {"Desperate": 0.6, "Resilient": 0.4},
    "China": {"Stability-Focused": 0.7, "Opportunistic": 0.3},
    "Russia": {"Leverage-Seeking": 0.65, "Committed": 0.35},
    "USA": {"Hawkish": 0.8, "Restrained": 0.2},
    "Israel": {"Proactive": 0.75, "Cautious": 0.25}
}

# 3. Actions
ACTIONS = {
    "Iran": ["Retaliate", "Negotiate", "Rebuild"],
    "China": ["Support Iran", "Remain Neutral", "Mediate"],
    "Russia": ["Support Iran", "Remain Neutral", "Disengage"],
    "USA": ["Escalate", "Maintain Pressure", "De-escalate"],
    "Israel": ["Escalate", "Maintain Pressure", "Pause"]
}

# 4. Payoff Matrices (Simplified)
# These are highly simplified and illustrative. A real model would require extensive data.
# Payoffs are structured as: PAYOFFS[player][player_type][iran_action][china_action][russia_action][usa_action][israel_action]

PAYOFFS = {
    player: {type: np.zeros((len(ACTIONS["Iran"]), len(ACTIONS["China"]), len(ACTIONS["Russia"]), len(ACTIONS["USA"]), len(ACTIONS["Israel"]))) for type in TYPES[player]} for player in PLAYERS
}

# Example Payoff Logic (to be populated based on geopolitical analysis)
# This is a placeholder for the complex payoff structure.
# For simplicity, we'll use a more abstract and simplified payoff logic in the simulation.

def get_payoff(player, player_type, action_profile):
    # A more sophisticated payoff function would be implemented here based on detailed analysis.
    # For this simulation, we'll use a simplified placeholder logic.
    # The logic will be based on a combination of the player's type and the actions of all players.

    payoff = 0
    iran_action, china_action, russia_action, usa_action, israel_action = action_profile

    if player == "Iran":
        if player_type == "Desperate":
            if iran_action == "Retaliate": payoff += 5
            if usa_action == "Escalate": payoff -= 5
        if player_type == "Resilient":
            if iran_action == "Negotiate": payoff += 5
            if iran_action == "Rebuild": payoff += 3

    if player == "China":
        if player_type == "Stability-Focused":
            if china_action == "Mediate": payoff += 5
            if usa_action == "Escalate" or iran_action == "Retaliate": payoff -= 3
        if player_type == "Opportunistic":
            if china_action == "Support Iran": payoff += 5
            if usa_action == "De-escalate": payoff -= 3

    if player == "Russia":
        if player_type == "Leverage-Seeking":
            if russia_action == "Support Iran": payoff += 3
            if usa_action == "Escalate": payoff += 2 # Creates more leverage
        if player_type == "Committed":
            if russia_action == "Support Iran": payoff += 5
            if usa_action == "Escalate": payoff -= 5

    if player == "USA":
        if player_type == "Hawkish":
            if usa_action == "Escalate": payoff += 5
            if iran_action == "Retaliate": payoff -= 5
        if player_type == "Restrained":
            if usa_action == "De-escalate": payoff += 5
            if iran_action == "Retaliate": payoff -= 5

    if player == "Israel":
        if player_type == "Proactive":
            if israel_action == "Escalate": payoff += 5
            if iran_action == "Retaliate": payoff -= 5
        if player_type == "Cautious":
            if israel_action == "Pause": payoff += 5
            if iran_action == "Retaliate": payoff -= 5

    return payoff

# Populate the PAYOFFS matrices
for player in PLAYERS:
    for type in TYPES[player]:
        for i, iran_action in enumerate(ACTIONS["Iran"]):
            for j, china_action in enumerate(ACTIONS["China"]):
                for k, russia_action in enumerate(ACTIONS["Russia"]):
                    for l, usa_action in enumerate(ACTIONS["USA"]):
                        for m, israel_action in enumerate(ACTIONS["Israel"]):
                            action_profile = (iran_action, china_action, russia_action, usa_action, israel_action)
                            PAYOFFS[player][type][i, j, k, l, m] = get_payoff(player, type, action_profile)





# 5. Game Simulation Logic

class GameState:
    def __init__(self, current_types, current_actions=None):
        self.current_types = current_types  # Dictionary: player -> assigned_type
        self.current_actions = current_actions if current_actions is not None else {}

    def __str__(self):
        type_str = ", ".join([f"{p}: {t}" for p, t in self.current_types.items()])
        action_str = ", ".join([f"{p}: {a}" for p, a in self.current_actions.items()])
        return f"Types: {{{type_str}}}\nActions: {{{action_str}}}"

def get_random_type(player):
    # Randomly assign a type to a player based on the defined probabilities
    type_options = list(TYPES[player].keys())
    probabilities = list(TYPES[player].values())
    return np.random.choice(type_options, p=probabilities)

def calculate_optimal_move(player, player_type, current_types, all_actions):
    # This function calculates the optimal move for a given player and their type,
    # considering the types of all other players. It assumes other players' actions
    # are unknown and will be chosen to maximize their own payoffs.
    # For simplicity, we'll assume a sequential decision-making process or a best-response
    # dynamic where each player chooses their action to maximize their payoff given the
    # current types and anticipating the *most likely* actions of others.
    # In a true Bayesian Nash Equilibrium, this would involve more complex iteration.

    best_action = None
    max_expected_payoff = -np.inf

    # Iterate through all possible actions for the current player
    for action in ACTIONS[player]:
        expected_payoff = 0

        # To calculate expected payoff, we need to consider all possible combinations
        # of actions from other players. This is computationally intensive for a full search.
        # For this simulation, we'll simplify: assume other players will also choose their
        # best action given their type, and we'll average over their possible actions.
        # This is a heuristic, not a true equilibrium calculation.

        # Create a temporary action profile to evaluate
        temp_action_profile = {
            "Iran": None, "China": None, "Russia": None, "USA": None, "Israel": None
        }
        temp_action_profile[player] = action

        # For other players, we'll consider their most likely optimal action given their type
        # This is a simplification; a full solution would involve nested best-response or fixed-point iteration.
        other_players_actions = {}
        for other_p in PLAYERS:
            if other_p != player:
                other_p_type = current_types[other_p]
                other_best_action = None
                other_max_payoff = -np.inf
                for other_p_action in ACTIONS[other_p]:
                    # This is a recursive simplification: assume others pick their best action
                    # without full knowledge of *our* current action choice, only types.
                    # This is a greedy approach for simulation, not a true game theory solution.
                    # For a proper solution, we'd need to solve for the Nash Equilibrium.
                    # Here, we're just picking the action that maximizes immediate payoff given types.
                    
                    # Construct a hypothetical action profile for evaluating other player's best move
                    hypothetical_action_profile = list(temp_action_profile.values())
                    # Fill in placeholders for other players' actions for this evaluation
                    # This part is tricky and requires careful indexing.
                    # Let's use a dictionary for action_profile for clarity.
                    
                    hypothetical_action_dict = {}
                    for p_idx, p_name in enumerate(PLAYERS):
                        if p_name == player:
                            hypothetical_action_dict[p_name] = action # Our current action
                        elif p_name == other_p:
                            hypothetical_action_dict[p_name] = other_p_action # Other player's potential action
                        else:
                            # For other players not being evaluated, we need a default or average.
                            # For simplicity, let's assume they pick their first action as a placeholder.
                            hypothetical_action_dict[p_name] = ACTIONS[p_name][0]

                    # Convert dict to tuple in fixed order for get_payoff
                    ordered_actions = tuple(hypothetical_action_dict[p] for p in PLAYERS)
                    
                    current_other_payoff = get_payoff(other_p, other_p_type, ordered_actions)
                    if current_other_payoff > other_max_payoff:
                        other_max_payoff = current_other_payoff
                        other_best_action = other_p_action
                other_players_actions[other_p] = other_best_action

        # Now, construct the full action profile for the current player's chosen action
        # and the *anticipated* best actions of others.
        final_action_profile_dict = other_players_actions.copy()
        final_action_profile_dict[player] = action
        
        # Convert dict to tuple in fixed order for get_payoff
        final_action_profile_tuple = tuple(final_action_profile_dict[p] for p in PLAYERS)

        current_payoff = get_payoff(player, player_type, final_action_profile_tuple)

        if current_payoff > max_expected_payoff:
            max_expected_payoff = current_payoff
            best_action = action

    return best_action

def simulate_step(current_state):
    print("\n--- Simulating New Step ---")
    print("Current Game State (Types):")
    for player, p_type in current_state.current_types.items():
        print(f"  {player}: {p_type}")

    optimal_moves = {}
    new_actions = {}

    # Players make their optimal moves based on current types
    for player in PLAYERS:
        player_type = current_state.current_types[player]
        # Pass all actions for indexing
        optimal_action = calculate_optimal_move(player, player_type, current_state.current_types, ACTIONS)
        optimal_moves[player] = optimal_action
        new_actions[player] = optimal_action

    new_state = GameState(current_state.current_types, new_actions)

    print("\nOptimal Moves for this Step:")
    for player, action in optimal_moves.items():
        print(f"  {player}: {action}")

    print("\nGame State After Moves:")
    print(new_state)

    return new_state


# Main Simulation Loop
if __name__ == "__main__":
    print("Starting Geopolitical Game Simulation...")

    # Initial State: Randomly assign types to all players
    initial_types = {player: get_random_type(player) for player in PLAYERS}
    current_game_state = GameState(initial_types)

    num_steps = 3  # Simulate for 3 steps

    for step in range(1, num_steps + 1):
        print(f"\n========== Step {step} ==========")
        current_game_state = simulate_step(current_game_state)

        # In a multi-step game, types or other parameters might evolve.
        # For this simulation, we'll keep types constant across steps to focus on action dynamics.
        # If the game were truly dynamic, types might change based on previous actions or external events.
        # For example, if Iran 'Rebuilds', its type might shift from 'Desperate' to 'Resilient' over time.
        # This would require a more complex state transition function.

    print("\nSimulation Complete.")



