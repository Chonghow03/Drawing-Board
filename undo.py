from __future__ import annotations
from action import PaintAction
from data_structures.stack_adt import ArrayStack
from grid import Grid


class UndoTracker:

# Explanation coding concept:
# Initialise the self.action_list to create a ArrayStack with 100000 capacity
# Initialise the self.undo_action to create a ArrayStack with 100000 capacity

# Time complexity analysis:
# ArrayStack which is O(max_capacity) since the parameter is a constant.
# Thus the time complexity is linear time O(1).
    def __init__(self):
        self.action_list = ArrayStack(1000)
        self.undo_action = ArrayStack(1000)

# Explanation coding concept:
# This add_function is add the action to the action_list.
# First, checking the action_list is full or not.
# If the action_list is full do nothing and return None.
# Otherwise, add the action to the action_list by implementing push method.

# Time complexity analysis:
# The is_full and push method is O(1).
# In worst case, O(1)*O(1)+O(1) = O(1).
# In best case, the action_list is full and return None, thus time complexity is O(1)
    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.
        """
        if not self.action_list.is_full():
            self.action_list.push(action)
        return None

# Explanation coding concept:
# This undo function is to undo the last action in action_list.
# First, checking the action_list is empty or not.
# If the action_list is empty, do nothing and return None.
# If the action_list is not empty, popping the top item in action_list.
# Then implementing undo_apply with the parameter grid.
# After undo, push the item into the undo_action for redo used.
# Returning undo at last.

# Time complexity analysis:
# Due to the is_empty method is O(1).So for the first comparison is O(1).
# The time complexity of pop, undo_apply, and push method is constant, so Big-O notation is O(1).
# For undo_apply function, if the draw style is sequence layer store, time complexity is O(n^2*Comp==). Otherwise, O(1)
# Worst case = O(1)*(O(1)+O(1)+O(1)+O(1)) =O(1)(For SET and ADD layer store) | O(1)*(O(1)+O(n^2*Comp==)+O(1)+O(1)) =O(n^2*Comp==)(For SEQUENCE layer store)
# In best case, the action_list is empty, thus just return statement which is O(1).
    def undo(self, grid: Grid) -> PaintAction | None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        :return: The action that was undone, or None.
        """
        if not self.action_list.is_empty():
            undo = self.action_list.pop()
            undo.undo_apply(grid)
            self.undo_action.push(undo)
            return undo
        return None

# Explanation coding concept:
# This function is to redo the last action done by undo.
# First, checking the undo_action is empty or not.
# If the undo_action is empty, then do nothing and return None.
# Otherwise, popping the top action in undo_action and assign it to redo variable.
# Apply the redo with redo_apply.
# After the action redo, pushing the redo variable to the action_list.
# Lastly, return the redo variable.

# Time complexity analysis:
# Due to the is_empty method is O(1).So for the first comparison is O(1).
# The time complexity of pop, redo_apply, and push method is constant, so Big-O notation is O(1).
# For redo_apply function, if the draw style is sequence layer store, time complexity is O(n^2*Comp==). Otherwise, O(1)
# Worst case = O(1)*(O(1)+O(1)+O(1)+O(1)) =O(1)(For SET and ADD layer store) | O(1)*(O(1)+O(n^2*Comp==)+O(1)+O(1)) =O(n^2*Comp==)(For SEQUENCE layer store)
# In best case, the action_list is empty, thus just return statement which is O(1).
    def redo(self, grid: Grid) -> PaintAction | None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        :return: The action that was redone, or None.
        """
        if not self.undo_action.is_empty():
            redo = self.undo_action.pop()
            redo.redo_apply(grid)
            self.action_list.push(redo)
            return redo
        return None
