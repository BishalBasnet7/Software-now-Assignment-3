"""
History Manager Class
Manages undo/redo functionality for image operations
Demonstrates encapsulation and state management
"""

import numpy as np


class HistoryManager:
    """
    Class responsible for managing the history of image states.
    Enables undo and redo functionality.
    """
    
    def __init__(self, max_history=20):
        """
        Constructor: Initialize the history manager.
        
        Args:
            max_history: Maximum number of states to keep in history
        """
        # Encapsulation: Private attributes
        self._history = []
        self._current_index = -1
        self._max_history = max_history
        
    def add_state(self, image_state):
        """
        Add a new image state to the history.
        
        Args:
            image_state: NumPy array representing the image state
        """
        # Remove any states after current index (if we're not at the end)
        if self._current_index < len(self._history) - 1:
            self._history = self._history[:self._current_index + 1]
        
        # Add the new state
        self._history.append(image_state.copy())
        self._current_index += 1
        
        # Limit history size
        if len(self._history) > self._max_history:
            self._history.pop(0)
            self._current_index -= 1
            
    def undo(self):
        """
        Undo to the previous state.
        
        Returns:
            Previous image state or None if no previous state exists
        """
        if self._current_index > 0:
            self._current_index -= 1
            return self._history[self._current_index].copy()
        return None
    
    def redo(self):
        """
        Redo to the next state.
        
        Returns:
            Next image state or None if no next state exists
        """
        if self._current_index < len(self._history) - 1:
            self._current_index += 1
            return self._history[self._current_index].copy()
        return None
    
    def get_current_state(self):
        """
        Get the current image state.
        
        Returns:
            Current image state or None if history is empty
        """
        if 0 <= self._current_index < len(self._history):
            return self._history[self._current_index].copy()
        return None
    
    def get_first_state(self):
        """
        Get the first (original) image state.
        
        Returns:
            First image state or None if history is empty
        """
        if len(self._history) > 0:
            return self._history[0].copy()
        return None
    
    def clear(self):
        """Clear all history."""
        self._history = []
        self._current_index = -1
        
    def can_undo(self):
        """
        Check if undo is possible.
        
        Returns:
            True if undo is possible, False otherwise
        """
        return self._current_index > 0
    
    def can_redo(self):
        """
        Check if redo is possible.
        
        Returns:
            True if redo is possible, False otherwise
        """
        return self._current_index < len(self._history) - 1
    
    def get_history_size(self):
        """
        Get the current size of the history.
        
        Returns:
            Number of states in history
        """
        return len(self._history)
    
    def get_current_index(self):
        """
        Get the current index in history.
        
        Returns:
            Current index
        """
        return self._current_index
