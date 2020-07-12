
'''
Created on Jul 12, 2020

@author: Artem Sotnikov
'''
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtCore import QRectF
from PyQt5.Qt import Qt


class GraphicsView(QGraphicsView):
    PAN_BOUNDARY = QRectF(-1500, -1000, 3000, 2000)
    
    
    def __init__(self):
        self.g_scene = QGraphicsScene()
        super().__init__(self.g_scene)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        
        self.g_scene.addRect(self.PAN_BOUNDARY)        
    
    def wheelEvent(self, event):   
#         print(event.angleDelta())  
        
        if (event.angleDelta().y() > 0):
            self.scale(1.2, 1.2)
        else:            self.scale(0.9, 0.9)