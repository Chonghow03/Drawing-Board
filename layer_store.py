from __future__ import annotations
from abc import ABC, abstractmethod

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

    def __init__(self):
        self.layer = None
        self.s=False

    def add(self,layer:Layer) ->bool:
        self.layer = layer
        return True

    def erase(self, layer: Layer) -> bool:
        self.layer = None
        return True

    def special(self):
        if self.s:
            self.s = False
        else:
            self.s = True

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        if self.layer==None:
            result=start
        else:
            result=self.layer.apply(start,timestamp,x,y)
        if self.s:
            result=invert.apply(result,timestamp,x,y)
        return result

class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """

    def __init__(self):
        self.myStack = None
        self.myStack = ArrayStack(1000)
        self.s = False

    def add(self, layer: Layer) -> bool:
        if self.myStack.is_full():
            return False
        else:
            self.myStack.push(layer)
            return True

    def erase(self, layer: Layer) -> bool:
        if self.myStack.is_empty():
            return False
        else:
            self.myStack.pop()
            return True

    def special(self):
        self.s = not self.s

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        if self.myStack is None:
            result = start
        else:
            result = self.myStack.apply(start,timestamp,x,y)
        if self.s:
            for i in range(len(self.myStack)):
                color = self.myStack.pop()
                result = self.myStack.push(color)
        return result



class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """

    pass
