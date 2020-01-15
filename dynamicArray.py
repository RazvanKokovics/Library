"""
Author: Kokovics Razvan-Florin (Kazvik)
Description: A DynamicArray Class implementation in Python with ShellSort based on a comparing function and a FilterMethod based on an acceptanceFunction.
"""

class DynamicArray():
    
    def __init__(self):
        #function that initializes a DynamicArray object
        self._current = 0
        self._capacity = 1
        self._elem = self.__create(self._capacity)
    
    def __create(self, capacity):
        #function that creates and returns a list filled by 'None' values.
        #The size of the list is given by the capacity variable. 
        #capacity - (integer)
        return [None] * capacity
    
    def __resize(self, new_capacity):
        #function that resizes a DynamicArray with a newcapacity.
        #newcapacity - (integer)
        new_array = self.__create(new_capacity)
        for i in range(self._current):
            new_array[i] = self._elem[i]
        self._elem = new_array
        self._capacity = new_capacity
    
    def append(self, data):
        #function that appends a new element to the DynamicArray.
        #data - (any type)
        if self._current == self._capacity:
            self.__resize(2 * self._capacity)
        self._elem[self._current] = data
        self._current = self._current + 1
    
    def __setitem__(self, index, data):
        #function that sets the value of an element from the DynamicArray at a given index.
        #raises an Exception if the index is out of range.
        #index - (integer)
        #data - (any type)
        if index >= self._current or index < 0:
            raise Exception("DynamicArray: index out of range!")
        else:
            self._elem[index] = data
    
    def __getitem__(self, index):
        #function that gets the value of an element from the DynamicArray at a given index.
        #raises an Exception if the index is out of range.
        #index - (integer)
        if index >= self._current or index < 0:
            raise Exception("DynamicArray: index out of range!")
        else:
            return self._elem[index]
    
    def __delitem__(self, index):
        #function that deletes an element from the DynamicArray at a given index.
        #raises an Exception if the index is out of range.
        #index - (integer)
        if index >= self._current or index < 0:
            raise Exception("DynamicArray: index out of range!")
        else:
            for i in range(index, self._current - 1):
                self._elem[i] = self._elem[i+1]
            self._current = self._current - 1
            if 4 * self._current == self._capacity:
                self.__resize(2 * self._current)
            
    def __next__(self, index):
        #function that gets the next element from the DynamicArray at a given index.
        #raises an Exception if the index is out of range.
        #index - (integer)
        if index >= self._current or index < 0:
            raise Exception("DynamicArray: index out of range!")
        else:
            return self._elem[index + 1]
    
    def __len__(self):
        #function that returns how many elements has the DynamicArray.
        return self._current
    
    def __iter__(self):
        #function that iterates through the DynamicArray.
        l = self._elem[:self._current]
        return l.__iter__()

    def shell_sort(self, function):
        #function that sorts the DynamicArray based on a function of comparing
        #function = the funcion used for comparing
        length = self._current
        gap = length // 2
        while gap > 0:
            for i in range(gap, length):
                aux = self._elem[i]
                j = i
                while j >= gap and function(self._elem[j - gap], aux):
                    self._elem[j] = self._elem[j - gap]
                    j = j - gap
                self._elem[j] = aux
            gap = gap // 2
    
    def filter(self, acceptanceFunction):
        #function that filters the DynamicArray based on an acceptanceFunction
        #acceptanceFunction = the function that checks if an element passes the filter
        #returns a list with all the elements that pass the given filter
        filteredList = []
        for i in range(self._current):
            if acceptanceFunction(self._elem[i]):
                filteredList.append(self._elem[i])
        return filteredList
                
        