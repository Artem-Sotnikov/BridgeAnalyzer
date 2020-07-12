'''
Created on Jul 12, 2020

@author: Artem Sotnikov
'''


from main_frame import MainFrame

import anastruct as anast

from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    print('Bridge Analyser active!')
    
    app = QApplication([])
    main_frame = MainFrame()

    app.exec()