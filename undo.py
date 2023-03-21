from __future__ import annotations
from action import PaintAction
from data_structures.stack_adt import ArrayStack
from grid import Grid


class UndoTracker:

# Initialise the self.action_list to create a ArrayStack with 100000 memories
# Initialise the self.undo_action to create a ArrayStack with 100000 memories
    def __init__(self):
        self.action_list = ArrayStack(100000)
        self.undo_action = ArrayStack(100000)

# This add_function is add the action to the action_list.
# First, checking the action_list is full or not.
# If the action_list is full do nothing and return None.
# Otherwise, add the action to the action_list by implementing push method.
    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.
        """
        if not self.action_list.is_full():
            self.action_list.push(action)
        return None

# This undo function is to undo the last action
# First, checking the action_list is empty or not.
# If the action_list is empty, do nothing and return None
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
