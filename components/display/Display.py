from abc import ABCMeta, abstractmethod


class Display(metaclass=ABCMeta):

    @abstractmethod
    void setPixel(int x, int y, Color color):
        '''
        Set a specific pixel for a color 

        @param x Row position. 0 is first, top to down direction
        @param y Column position. 0 is first, left to right direction
        @param color
        '''
        ...

    @abstractmethod
    void redraw():
        '''
        Repaint the display, updating changes caused by use of setPixel method
        '''
        ...

    @abstractmethod
    void clear():
        '''
        Change the Display for initial stage
        '''
        ...

    @abstractmethod
    int getWidth():
        ...
    
    @abstractmethod
    int getHeight():
        ...
}
