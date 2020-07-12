'''
Created on Jul 12, 2020

@author: Artem Sotnikov
'''

from PyQt5.QtWidgets import QFrame, QVBoxLayout
from graphics_view import GraphicsView



class MainFrame(QFrame):    
    def __init__(self):
        super().__init__()
        
        #self.menu_bar = MainFrameMenubar()
        self.graphics_widget = GraphicsView()
        
        print('main window created')
        self.setLayout(QVBoxLayout())
        #self.layout().addWidget(self.menu_bar)
        self.layout().addWidget(self.graphics_widget)
        
        self.show()