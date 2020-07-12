'''
Created on Jul 12, 2020

@author: Artem Sotnikov
'''

import csv
import anastruct as ans
from anastruct import Vertex

class DataExtractor():
    def __init__(self):
        pass
    
    def extract_data(self, file_path):
        csvfile = open(file_path, newline='')
        reader = list(csv.reader(csvfile))
        
        output_list = []
        
        for row in reader[1:]:
            end_vertex = (float(row[2]), float(row[3]))
            start_vertex = (float(row[4]), float(row[5]))
            
            ins_list = [start_vertex, end_vertex]
            output_list.append(ins_list)

        print(output_list)
        return output_list
# Test
#extractor = DataExtractor()
#extractor.extract_data(r"C:/Users/Artem Sotnikov/Documents/test_data_extract3.csv")
