from __future__ import annotations
from abc import ABC, abstractmethod

from data_structures.array_sorted_list import ArraySortedList
from data_structures.queue_adt import CircularQueue
from data_structures.sorted_list_adt import ListItem
from data_structures.stack_adt import ArrayStack
from layer_util import Layer
from layers import invert


class LayerStore(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass


class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """
# Explanation coding concept:
# Initialise the self.layer is equal to None
# Initialise the self.s for judging the switch of special to False

# Time complexity analysis:
# O(1)(Assignment)+O(1)(Assignment) = O(1) (Linear time)
# Best case = Worst case
    def __init__(self):
        self.layer = None
        self.s = False

# Explanation coding concept:
# This function is to add the layer to self.layer
# If the layer added successfully, return True

# Time complexity analysis:
# O(1)(Assignment)+O(1)(Return statement) = O(1) (Linear time)
# Best case = Worst case
    def add(self, layer: Layer) -> bool:
        self.layer = layer
        return True

# Explanation coding concept:
# This function is to remove the layer from self.layer
# Due to the self.layer is equal to layer after adding, i just need to set self.layer to None
# Thus the layer removed successfully and return True

# Time complexity analysis:
# O(1)(Assignment)+O(1)(Return statement) = O(1) (Linear time)
# Best case = Worst case
    def erase(self, layer: Layer) -> bool:
        self.layer = None
        return True

# Explanation coding concept:
# This function is acting like a switch
# If user apply this special function, I just need to change the boolean of self.s by using not
# If the function is called, self.s = True will change to self.s = False
# Otherwise, self.s = False will change to self.s = True

# Time complexity analysis:
# O(1)(Assignment) (Linear time)
# Best case = Worst case
    def special(self):
        self.s = not self.s

# Explanation coding concept:
# This function is to reflect the colour this square should show, given the current layers.
# If the self.layer is nothing, result is equal to start which is the tuple of the color.
# Otherwise, I call the apply function with the start, timestamp,x and y parameters to apply a tuple of the color.
# After getting a result, if the user activate the special effect,
# I will call the invert and apply function to invert the result.
# Returning the result at last.

# Time complexity analysis:
# Worst case: O(1)(Comp==)*O(1)(Assignment and apply function) + O(1)(Comp==)*O(Assignment and apply function) + O(1) (Return statement) = O(1) (constant)
# Best case = Worst case = O(1) (Indeed!)

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        if self.layer is None:
            result = start
        else:
            result = self.layer.apply(start, timestamp, x, y)
        if self.s:
            result = invert.apply(result, timestamp, x, y)
        return result


class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """

# Explanation coding concept:
# Initialise the self.myQueue by using the CircularQueue ADT
# Initialise the self.myStack by using the ArrayStack ADT

# Time complexity analysis:
# It depends on CircularQueue and ArrayStack which are O(max_capacity) since the parameter is a constant.
# Thus the time complexity is linear time O(1).
# O(1)(Assignment)+O(1)(Assignment) = O(1) (Linear time)
# Best case = Worst case
    def __init__(self):
        self.myQueue = CircularQueue(10000)
        self.myStack = ArrayStack(10000)

# Explanation coding concept:
# This add function is to add the layer into the queue (self.myQueue)
# Before adding the layer into the queue,
# I have to check the queue has space to add or not by using is_full() abstract method.
# If myQueue is full, then return False and do nothing, otherwise,
# return True and add the layer into myQueue by using append method.

# Time complexity analysis:
# All return statements, assignments and integer comparisons in append method are always constant, hence O(1).
# Worst case: O(1)(Comp==) + O(1)(append)+O(1)(Return statement) = O(1) (Linear time)
# Best case: If myQueue is full and just return False without append method.
# O(1)(Comp==) + O(1)(Return statement) = O(1) (Linear time)
    def add(self, layer: Layer) -> bool:
        if self.myQueue.is_full():
            return False
        else:
            self.myQueue.append(layer)
            return True

# Explanation coding concept:
# This erase function is to remove the layer which located at the top of the queue.
# First, I check the queue is empty or not. ("Does the queue has something to erase?")
# If myQueue is empty, then return False and do nothing.
# Otherwise, return True and remove the last adding layer by using serve method.

# Time complexity analysis:
# All return statements, assignments and integer comparisons in serve method are always constant, hence O(1).
# Worst case: O(1)(Comp==) + O(1)(append)+O(1)(Return statement) = O(1) (Linear time)
# Best case: If myQueue is full and just return False without serve method.
# O(1)(Comp==) + O(1)(Return statement) = O(1) (Linear time)
    def erase(self, layer: Layer) -> bool:
        if self.myQueue.is_empty():
            return False
        else:
            self.myQueue.serve()
            return True

# Explanation coding concept:
# This special function is to reverse the order of all the layer in myQueue.
# The first for loop is to move all the elements in myQueue to myStack by using serve and push method.
# So now, we have the original order of layer in myStack.
# The second for loop is to reverse the order of layer in myStack by using pop method
# Due to Stack item is first in last out, loop through all the layer by popping the last layer and appending back to myQueue.
# After dealing all the reversing, return myQueue

# Time complexity analysis:
# Worst case: O(len(self.myQueue))(1st for loop)*O(1)(serve,assignment and push)
# + O(len(self.myStack))(2nd for loop)*O(1)O(1)(pop,assignment and append) + O(1)(return statement)
# Let size of self.myQueue = n and size of self.myStack = m
# In Big-O notation, the time complexity is O(n+m)
# Best case = Worst case
    def special(self):
        for i in range(len(self.myQueue)):
            color = self.myQueue.serve()
            self.myStack.push(color)
        for j in range(len(self.myStack)):
            stack = self.myStack.pop()
            self.myQueue.append(stack)
        return self.myQueue

# Explanation coding concept:
# If the length of myQueue is not empty, I apply a for loop to obtain the tuple of color of each layer in the queue.
# In the for loop, variable queue is the layer after serving in myQueue.
# Then obtain the color by using apply function.
# After using, append the layer back to the queue.
# At last return the tuple of all color

# Time complexity analysis:
# Worst case: The len(self.myQueue) is not 0, O(1)(Comp==) + O(len(self.myQueue)*O(1)(All assignments, serve, apply and append are constant)
# + O(1) (return statement)
# Let the length of self.myQueue be n, thus the worst case time complexity is O(n).
# Best case is length of self.myQueue is 0, then return start.
# Therefore, the time complexity of best case is O(1).
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        if len(self.myQueue) != 0:
            for i in range(len(self.myQueue)):
                queue = self.myQueue.serve()
                start = queue.apply(start, timestamp, x, y)
                self.myQueue.append(queue)
        return start


class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """

# Explanation coding concept:
# Initialise the self.mySortedlist by using the ArraySortedList ADT
# Initialise the self.lexicographic_list by using the ArraySortedList ADT

# Time complexity analysis:
# It depends on ArraySortedList which are O(max_capacity) since the parameter is a constant.
# Thus the time complexity is linear time O(1).
# O(1)(Assignment)+O(1)(Assignment) = O(1) (Linear time)
# Best case = Worst case
    def __init__(self):
        self.mySortedlist = ArraySortedList(10000)
        self.lexicographic_list = ArraySortedList(10000)

# Explanation coding concept:
# Before adding the layer into mySortedlist, I have to check the layer is applied in mySortedlist before or not.
# Due to mySortedlist is add by the form of list, so if I have to deal with the layer in mySortedlist,
# I must utilise LIstItem form to add in.
# If the list item with two parameters(layer and its index) is not in mySortedlist,
# I will add the LIstItem with the layer and its index into mySortedlist by using add abstract method.
# If added, return True, otherwise, return False.

# Time complexity analysis:
# In add function, worst case is self.mySortedlist is full and needed to resize and the item to be found the position is at first.
# The worst case time complexity of resize is O(len(self.mySortedlist))
# If item is first, we get O(log len(self.mySortedlist)) + O(len(self.mySortedlist)), which gives O(len(self.mySortedlist))
# Worst case: O(1)(Comp=)*O(O(len(self.mySortedlist))) + O(len(self.mySortedlist))(index_to_add method) + O(1)(Assignment) + O(1)(Numerical operation)
# Let n be the length of mySortedlist
# Thus, the time complexity in worst case is O(n+n) = O(n)
# For best case the self.mySortedlist is not full and the item position is at the last.
# For self._index_to_add, if item is last, we get O(log len(self.mySortedlist)) + O(1) which gives O(log len(self.mySortedlist)).
# Best case: O(1)(Comp==) + O(log len(self.mySortedlist))(index_to_add method) + O(1)(Assignment) + O(1)(Numerical operation)
# Hence, the time complexity in best case is O(log n)

# From above add method in array_sorted_list data structure, the time complexity in worst case is O(n),in best case is O(log n).
# Worst case for whole function: O(n*Comp==)*(O(n)+O(1)) = O(n^2*Comp==)
# Best case: O(1)(Return statement) (layer is added in the list before.)
    def add(self, layer: Layer) -> bool:
        if ListItem(layer,layer.index) not in self.mySortedlist:
            self.mySortedlist.add(ListItem(layer, layer.index))
            return True
        return False

# Explanation coding concept:
# Before removing the layer out mySortedlist, I have to check the layer is contained in mySortedlist or not.
# If list item of layer is contained in mySortedlist,
# I can remove the it by using remove abstract method in sorted_list_adt.
# If removed, return True, otherwise, return False.

# Time complexity analysis:
    # For delete_at_index function,
    # Worst case: O(n-index)
    # Best case: O(1) (index >=len(self))

    # For index function,
    # Worst case: O(n) (_index_to_add method)
    # Best case: O(log n) (_index_to_add method)

    #Thus, for remove function,
    # Worst case: O(n)
    # Best case: O(log n)
# Let the size of self.mySortedlist be n
# Worst case: O(n*Comp==)*(O(n)+O(1)) = O(n^2*Comp==)
# Best case: O(1) (Return statement) (layer is not in the list)
    def erase(self, layer: Layer) -> bool:
        if self.mySortedlist.__contains__(ListItem(layer, layer.index)):
            self.mySortedlist.remove(ListItem(layer,layer.index))
            return True
        return False

# Time complexity analysis:
# Let n be the length of mySortedlist
# Let m be the length of lexicographic_list
# Worst case: O(n)(1st for loop) *O(n)(add function) +O(1)(clear) +O(1)(assignment and numerical operations)
# +O(n-index_of_median)(delete_at_index) +O(m)(2nd for loop) *O(m)(add function) +O(1)(clear) + O(1)(return statement)
# Thus, the worst case of time complexity is O(n^2+m^2)
# Best case: O(1) (self.mySortedList is empty and return None)
    def special(self):
# Explanation coding concept:
# If the mySortedlist is empty, then return None, otherwise applied the special effect.
# The first for loop is to copy the elements in mySortedlist to lexicographic_list with the order of the value name.
# Thus, the value of the list item is self.mySortedlist[i].value and the key is the value name.
# After moving all the list item to lexicographic_list, I clear all the list item in mySortedlist by using clear method.
        if self.mySortedlist.is_empty():
            return None

        for i in range(len(self.mySortedlist)):
            self.lexicographic_list.add(ListItem(self.mySortedlist[i].value, self.mySortedlist[i].value.name))
        self.mySortedlist.clear()

# Explanation coding concept:
# First, I set the index_of_median is the index of half length of lexicographic_list (the index of centre elements)
# Based on the index_of_median, removing the list item by using delete_at_index abstract method.
# The last for loop is to add the list item in lexicographic_list back to the mySortedlist with the order by their index.
# Thus, the value of ListItem is self.lexicographic_list[j].value and the key is self.lexicographic_list[j].value.index.
# After using, clear the item in lexicographic_list by using clear method.
# Returning mySortedlist at last.
        index_of_median = (len(self.lexicographic_list)-1)// 2
        self.lexicographic_list.delete_at_index(index_of_median)

        for j in range(len(self.lexicographic_list)):
            self.mySortedlist.add(ListItem(self.lexicographic_list[j].value, self.lexicographic_list[j].value.index))
        self.lexicographic_list.clear()
        return self.mySortedlist

# Explanation coding concept:
# If the length of mySortedlist is not equal to 0, implementing the get_color effect.
# The for loop is to loop through mySortedlist by the length number.
# The variable color assigned is to obtain the value of mySortedlist in every loop.
# Then, obtain the tuple of the color by using apply function.
# Returning the start at last.

# Time complexity analysis:
# Worst case:O(1)(Comp==) * O(n)(1st for loop) * O(1)(All assignment,apply function and return statement) = O(n)
# Best case: O(1) (return statement) (When n is 0)
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        if len(self.mySortedlist) != 0:
            for i in range(len(self.mySortedlist)):
                color = self.mySortedlist[i].value
                start = color.apply(start, timestamp, x, y)
        return start
