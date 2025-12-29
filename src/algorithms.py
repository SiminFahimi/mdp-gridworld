import random
import time

from mdp import MDP, State


def value_iteration(mdp: MDP):
    policy = {state: "" for state in mdp.states}
    utility = {state: 0 for state in mdp.states}

    utility[State(mdp.grid, mdp.grid.hell)] = -1
    utility[State(mdp.grid, mdp.grid.heaven)] = 1

    converge = False
    threshold = 10 ** -4 * (1 - mdp.discount_factor) / mdp.discount_factor

    while not converge:
        converge = True
        for state in mdp.states:
            if mdp.is_wall_hell_heaven(state.position):
                continue

            old_value = utility[state]

            max_value = float("-inf")
            best_action = None
            for action in mdp.Actions.keys():
                sum_value = mdp.rewardfunction(state) + mdp.discount_factor * sum(
                    mdp.transitionmodel(state, action, other_state)
                    * utility[other_state]
                    for other_state in mdp.neighbor_states(state, action).values()
                )

                if sum_value > max_value:
                    max_value = sum_value
                    best_action = action

            utility[state] = max_value
            policy[state] = best_action

            if abs(utility[state] - old_value) > threshold:
                converge = False

    mdp.action_map_value_iteration = policy
    return [
        (state.position, round(utility[state], 2), policy.get(state, ""))
        for state in mdp.states
    ]


def policy_evaluation(policy: dict, expected_utility: dict, mdp: MDP):
    converge = False
    k = 0
    threshold = 1e-3

    while not converge and k < 10:
        k += 1
        converge = True
        for state in mdp.states:
            if mdp.is_wall_hell_heaven(state.position):
                continue

            old_value = expected_utility[state]
            action = policy[state]
            expected_utility[state] = mdp.rewardfunction(
                state
            ) + mdp.discount_factor * sum(
                mdp.transitionmodel(state, action, other_state)
                * expected_utility[other_state]
                for other_state in mdp.neighbor_states(state, action).values()
            )

            if abs(expected_utility[state] - old_value) > threshold:
                converge = False

    return expected_utility


def policy_iteration(mdp: MDP):
    policy = {state: random.choice(list(mdp.Actions.keys())) for state in mdp.states}
    expected_utility = {state: 0 for state in mdp.states}

    expected_utility[State(mdp.grid, mdp.grid.heaven)] = 1
    expected_utility[State(mdp.grid, mdp.grid.hell)] = -1

    unchanged = False
    while not unchanged:
        expected_utility = policy_evaluation(policy, expected_utility, mdp)
        unchanged = True

        for state in mdp.states:
            if mdp.is_wall_hell_heaven(state.position):
                continue

            old_action = policy[state]
            max_value = float("-inf")
            best_action = None

            for action in mdp.Actions.keys():
                sum_value = mdp.rewardfunction(
                    state
                ) + mdp.discount_factor * sum(
                    mdp.transitionmodel(state, action, other_state)
                    * expected_utility[other_state]
                    for other_state in mdp.neighbor_states(state, action).values()
                )

                if sum_value > max_value:
                    max_value = sum_value
                    best_action = action

            if best_action != old_action and expected_utility[state] < max_value:
                policy[state] = best_action
                unchanged = False

    mdp.action_map_policy_iteration = policy
    return [
        (state.position, round(expected_utility[state], 2), policy.get(state, ""))
        for state in mdp.states
    ]


def elapsed_time(func):
    start = time.perf_counter()
    func()
    end = time.perf_counter()
    return end - start


def time_compareness(grid_factory):
    time_policy_iteration = {}
    time_value_iteration = {}

    wall_density = [ 2 / 10, 3 / 10, 4 / 10]
    grid_sizes = [(20,20),(30,30),(100,100)]

    num_trials = 3

    for size in grid_sizes:
        x, y = size
        for density in wall_density:
            grid = grid_factory(x, y, 10, density)
            mdp = MDP(grid, 0.2, 0.9)

            policy_times = 0
            value_times = 0

            for _ in range(num_trials):
                policy_times += elapsed_time(lambda: policy_iteration(mdp))
                value_times += elapsed_time(lambda: value_iteration(mdp))

            time_policy_iteration[((x, y), density)] = policy_times / num_trials
            time_value_iteration[((x, y), density)] = value_times / num_trials

    return time_policy_iteration, time_value_iteration
