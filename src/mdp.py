from dataclasses import dataclass

from grid import Grid


class Robot_Agent:
    def __init__(self, position):
        self.position = position
        self.reward = 0


@dataclass(frozen=True)
class State:
    grid: Grid
    position: tuple

    def __hash__(self):
        return hash(self.position)


class MDP:
    def __init__(self, grid: Grid, noise: float, discount_factor: float):
        self.grid = grid
        self.noise = noise
        self.discount_factor = discount_factor

        self.states = [
            State(self.grid, (x, y))
            for x in range(0, self.grid.screen_width, self.grid.cell_size)
            for y in range(0, self.grid.screen_height, self.grid.cell_size)
        ]

        self.Actions = {
            "right": (self.grid.cell_size, 0),
            "up": (0, -1 * self.grid.cell_size),
            "left": (-1 * self.grid.cell_size, 0),
            "down": (0, self.grid.cell_size),
        }

        self.transitions = {}
        self.action_map_value_iteration = None
        self.action_map_policy_iteration = None

        self.precalculate_transitions()

    @staticmethod
    def possible_action(action: str):
        possible_actions = {
            "down": ["left", "right"],
            "up": ["left", "right"],
            "left": ["up", "down"],
            "right": ["up", "down"],
        }
        return possible_actions[action] + [action]

    def is_wall_hell_heaven(self, position):
        return (
            position in self.grid.walls
            or position == self.grid.hell
            or position == self.grid.heaven
        )

    def is_valid_position(self, position):
        return (
            position not in self.grid.walls
            and 0 <= position[0] < self.grid.screen_width
            and 0 <= position[1] < self.grid.screen_height
        )

    def neighbor_states(self, state: State, action: str):
        neighbor_states = {}
        for possible_action in self.possible_action(action):
            dx, dy = self.Actions[possible_action]
            new_position = (state.position[0] + dx, state.position[1] + dy)
            if self.is_valid_position(new_position):
                neighbor_states[possible_action] = State(self.grid, new_position)
            else:
                neighbor_states[possible_action] = state
        return neighbor_states

    def calculate_transition_probability(self, state, action, other_state):
        neighbors = self.neighbor_states(state, action).items()
        for possible_action, another_state in neighbors:
            if other_state == another_state:
                return (
                    1 - self.noise
                    if possible_action == action
                    else self.noise / 2
                )
        return 0

    def precalculate_transitions(self):
        self.transitions = {}
        for state in self.states:
            for action in self.Actions:
                for other_state in self.neighbor_states(state, action).values():
                    probability = self.calculate_transition_probability(
                        state, action, other_state
                    )
                    if probability > 0:
                        self.transitions[(state, action, other_state)] = probability

    def transitionmodel(self, state, action, other_state):
        return self.transitions[(state, action, other_state)]

    def rewardfunction(self, state: State):
        if state.position == self.grid.hell:
            return -1
        elif state.position == self.grid.heaven:
            return 1
        else:
            return 0
