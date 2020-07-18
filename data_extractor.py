'''
Created on Jul 12, 2020

@author: Artem Sotnikov
'''

import csv
import anastruct as ans
from anastruct import Vertex

class DataExtractor():
    DEBUG_MODE = True
    
    def __init__(self):
        pass
    
    def extract_data(self, file_path):
        csvfile = open(file_path, newline='')
        reader = list(csv.reader(csvfile))
        
        output_list = []
        
        label_table = reader[0]
        if (self.DEBUG_MODE):
            print('\nDataExtractor label table:')
            print(label_table)
        
        for idx, itm in enumerate(label_table): 
            if (itm == 'End X'):
                end_vertex_x_idx = idx
            if (itm == 'End Y'):
                end_vertex_y_idx = idx
            if (itm == 'Start X'):
                start_vertex_x_idx = idx
            if (itm == 'Start Y'):
                start_vertex_y_idx = idx
            if (itm == 'Length'):
                length_idx = idx
         
        
        for row in reader[1:]:
            end_vertex = (float(row[end_vertex_x_idx]), float(row[end_vertex_y_idx]))
            start_vertex = (float(row[start_vertex_x_idx]), float(row[start_vertex_y_idx]))
            
            ins_list = [start_vertex, end_vertex, float(row[length_idx])]
            output_list.append(ins_list)
        if (self.DEBUG_MODE):
            print('\nDataExtractor raw output:')
            print(output_list)
        return output_list

if __name__ == '__main__':
    # Test
    extractor = DataExtractor()
    extractor.extract_data(r"C:/Users/Artem Sotnikov/Documents/test_data_extract3.csv")

