from library import utilities


class SearchProblem:
    def get_start_state(self):
        utilities.raise_not_defined()

    def is_goal_state(self, state):
        utilities.raise_not_defined()

    def get_successors(self, state):
        utilities.raise_not_defined()

    def get_cost_of_actions(self, actions):
        utilities.raise_not_defined()
