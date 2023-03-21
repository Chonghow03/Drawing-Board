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

# Initialise the self.layer is equal to None
# Initialise the self.s for judging the switch of special to False
    def __init__(self):
        self.layer = None
        self.s = False

# This function is to add the layer to self.layer
# If the layer added successfully, return True
    def add(self, layer: Layer) -> bool:
        self.layer = layer
        return True

# This function is to remove the layer from self.layer
# Due to the self.layer is equal to layer after adding, i just need to set self.layer to None
# Thus the layer removed successfully and return True
    def erase(self, layer: Layer) -> bool:
        self.layer = None
        return True

# This function is acting like a switch
# If user apply this special function, I just need to change the boolean of self.s by using not
# If the function is called, self.s = True will change to self.s = False
# Otherwise, self.s = False will change to self.s = True
    def special(self):
        self.s = not self.s

# This function is to reflect the colour this square should show, given the current layers.
# If the self.layer is nothing, result is equal to start which is the tuple of the color.
# Otherwise, I call the apply function with the start, timestamp,x and y parameters to apply a tuple of the color.
# After getting a result, if the user activate the special effect,
# I will call the invert and apply function to invert the result.
# Returning the result at last.
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

# Initialise the self.myQueue by using the CircularQueue ADT
# Initialise the self.myStack by using the ArrayStack ADT
    def __init__(self):
        self.myQueue = CircularQueue(100000)
        self.myStack = ArrayStack(100000)

# This add function is to add the layer into the queue (self.myQueue)
# Before adding the layer into the queue,
# I have to check the queue has space to add or not by using is_full() abstract method.
# If myQueue is full, then return False and do nothing, otherwise,
# return True and add the layer into myQueue by using append method.
    def add(self, layer: Layer) -> bool:
        if self.myQueue.is_full():
            return False
        else:
            self.myQueue.append(layer)
            return True

# This erase function is to remove the layer which located at the top of the queue.
# First, I check the queue is empty or not. ("Does the queue has something to erase?")
# If myQueue is empty, then return False and do nothing.
# Otherwise, return True and remove the last adding layer by using serve method.
    def erase(self, layer: Layer) -> bool:
        if self.myQueue.is_empty():
            return False
        else:
            self.myQueue.serve()
            return True

# This special function is to reverse the order of all the layer in myQueue.
# The first for loop is to move all the elements in myQueue to myStack by using serve and push method.
# So now, we have the original order of layer in myStack.
# The second for loop is to reverse the order of layer in myStack by using pop method
# Due to Stack item is first in last out, loop through all the layer by popping the last layer and appending back to myQueue.
# After dealing all the reversing, return myQueue
    def special(self):
        for i in range(len(self.myQueue)):
            color = self.myQueue.serve()
            self.myStack.push(color)
        for j in range(len(self.myStack)):
            stack = self.myStack.pop()
            self.myQueue.append(stack)
        return self.myQueue

# If the length of myQueue is not empty, I apply a for loop to obtain the tuple of color of each layer in the queue.
# In the for loop, variable queue is the layer after serving in myQueue.
# Then obtain the color by using apply function.
# After using, append the layer back to the queue.
# At last return the tuple of all color
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

# Initialise the self.mySortedlist by using the ArraySortedList ADT
# Initialise the self.lexicographic_list by using the ArraySortedList ADT
    def __init__(self):
        self.mySortedlist = ArraySortedList(100000)
        self.lexicographic_list = ArraySortedList(100000)

# Before adding the layer into mySortedlist, I have to check the layer is applied in mySortedlist before or not.
# Due to mySortedlist is add by the form of list, so if I have to deal with the layer in mySortedlist,
# I must utilise LIstItem form to add in.
# If the list item with two parameters(layer and its index) is not in mySortedlist,
# I will add the LIstItem with the layer and its index into mySortedlist by using add abstract method.
# If added, return True, otherwise, return False.
    def add(self, layer: Layer) -> bool:
        if ListItem(layer,layer.index) not in self.mySortedlist:
            self.mySortedlist.add(ListItem(layer, layer.index))
            return True
        return False

# Before removing the layer out mySortedlist, I have to check the layer is contained in mySortedlist or not.
# If list item of layer is contained in mySortedlist,
# I can remove the it by using remove abstract method in sorted_list_adt.
# If removed, return True, otherwise, return False.
    def erase(self, layer: Layer) -> bool:
        if self.mySortedlist.__contains__(ListItem(layer, layer.index)):
            self.mySortedlist.remove(ListItem(layer,layer.index))
            return True
        return False

# If the mySortedlist is empty, then return None, otherwise applied the special effect.
# The first for loop is to copy the elements in mySortedlist to lexicographic_list with the order of the value name.
# Thus, the value of the list item is self.mySortedlist[i].value and the key is the value name.
# After moving all the list item to lexicographic_list, I clear all the list item in mySortedlist by using clear method.
    def special(self):
        if self.mySortedlist.is_empty():
            return None

        for i in range(len(self.mySortedlist)):
            self.lexicographic_list.add(ListItem(self.mySortedlist[i].value, self.mySortedlist[i].value.name))
        self.mySortedlist.clear()

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

# If the length of mySortedlist is not equal to 0, implementing the get_color effect.
# The for loop is to loop through mySortedlist by the length number.
# In line 231, the purpose is to obtain the value of mySortedlist in every loop.
# Then, obtain the tuple of the color by using apply function.
# Returning the start at last.
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        if len(self.mySortedlist) != 0:
            for i in range(len(self.mySortedlist)):
                color = self.mySortedlist[i].value
                start = color.apply(start, timestamp, x, y)
        return start
