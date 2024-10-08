from __future__ import annotations
from action import PaintAction
from data_structures.queue_adt import CircularQueue
from grid import Grid


class ReplayTracker:

# Explanation coding concept:
# Initialise self.replay_action to create a CircularQueue.

# Complexity analysis:
# It depends on CircularQueue which is O(max_capacity) since the parameter is a constant.
# Thus the time complexity is linear time O(1).
    def __init__(self):
        self.replay_action = CircularQueue(10000)

    def start_replay(self) -> None:
        """
        Called whenever we should stop taking actions, and start playing them back.

        Useful if you have any setup to do before `play_next_action` should be called.
        """
        pass

# Explanation coding concept:
# This add_action is to add the action and is_undo boolean into replay_action.
# To add this to parameters into the circularqueue, I use append method to add the tuple of two items into it.

# Complexity analysis:
# This operation takes a constant amount of time,
# The algorithm performs the constant time of running the whole function in best and worst case.
# Therefore, the best case and worst case of time complexity of add_function is O(1).
    def add_action(self, action: PaintAction, is_undo: bool = False) -> None:
        """
        Adds an action to the replay.

        `is_undo` specifies whether the action was an undo action or not.
        Special, Redo, and Draw all have this is False.
        """
        self.replay_action.append((action, is_undo))


# Explanation coding concept:
# Checking the replay_action is empty or not.
# If the replay_action is empty, means there is no action to replay, thus return False.
# Otherwise, serve the first item in replay_action and assign it to action variable.
# If the second element (boolean of is_undo) in action is True, the first element of action applied undo_apply function.
# Otherwise, the first element of action applied redo_apply function with parameter grid.
# If there have actions to play, return True.
# Otherwise, return False.

# Complexity analysis:
# In worst case,
# the first if statement performs O(1) (True or False). The serve action of the time complexity is O(1).
# The time complexity of the second comparison is O(1)*O(1) (redo_apply and undo_apply). And the return statement is O(1).
# Thus, the worst case of time complexity is O(1)*O(1)+O(1)*O(1)+O(1) =O(1) (Linear time)
# Due to the time complexity of worst case is O(1). Therefore, in best case (replay_action is empty) is definitely O(1).
    def play_next_action(self, grid: Grid) -> bool:
        """
        Plays the next replay action on the grid.
        Returns a boolean.
            - If there were no more actions to play, and so nothing happened, return True.
            - Otherwise, return False.
        """
        if not self.replay_action.is_empty():
            action = self.replay_action.serve()
            if not action[1]:
                action[0].redo_apply(grid)
            else:
                action[0].undo_apply(grid)
            return False
        return True


if __name__ == "__main__":
    action1 = PaintAction([], is_special=True)
    action2 = PaintAction([])

    g = Grid(Grid.DRAW_STYLE_SET, 5, 5)

    r = ReplayTracker()
    # add all actions
    r.add_action(action1)
    r.add_action(action2)
    r.add_action(action2, is_undo=True)
    # Start the replay.
    r.start_replay()
    f1 = r.play_next_action(g)  # action 1, special
    f2 = r.play_next_action(g)  # action 2, draw
    f3 = r.play_next_action(g)  # action 2, undo
    t = r.play_next_action(g)  # True, nothing to do.
    assert (f1, f2, f3, t) == (False, False, False, True)
