import pandas as pd
import numpy as np
import time

#this is simulating serial output from a csv and can be removed eventually
class simulation:
    values = []
    num_values_emitted = 0

    def __init__(self, values = []):
        self.values = values
        self.num_values_emitted = 0

    def read_value(self):
        time.sleep(.001)
        if (self.num_values_emitted < len(self.values[0])):
            self.num_values_emitted = self.num_values_emitted + 1
            return [place_holder[self.num_values_emitted - 1] for place_holder in self.values]
        else:
            return []
#well classes
class all_wells:
    def __init__(self):
        self.dict = {}
    def well_dictionary(self, list):
        self.dict = {
        for x in range(len(list)):
            x: str(list[x])
    }
class well:

    def __init__(self):
        self.impedance_buffered_values = list()
        self.impedance_current_value = 0
        self.impedance_count = 0
        self.buffer_size = 5
        self.embryo_status = False
        self.embryo_monitoring_bool = False
        self.embryo_reading_counter = 0
        self.average_first = 0
        self.average_second = 0
        self.count = 2

    def assign_value(self, argument_value):
        self.impedance_current_value = argument_value
        if len(self.impedance_buffered_values) < self.buffer_size:
            self.impedance_buffered_values.append(argument_value)
            self.impedance_count += 1
        self.impedance_buffered_values = self.impedance_buffered_values[1:]
        self.impedance_buffered_values.append(argument_value)
        self.impedance_count += 1
        if(np.absolute(self.impedance_buffered_values[-1] - self.impedance_buffered_values[0]) > 75):
            self.average_first = sum(self.impedance_buffered_values)/len(self.impedance_buffered_values)
            print("first average", self.average_first)
            self.buffer_flush()
            self.embryo_monitoring_bool = True
        if self.embryo_monitoring_bool == True:
            self.embryo_reading_counter += 1
        if(self.embryo_reading_counter == 4):
            self.average_second =  sum(self.impedance_buffered_values) / len(self.impedance_buffered_values)
            print("second average", self.average_second)
            print("average difference", np.absolute(self.average_second - self.average_first))
            print("time", spreadsheet["TIME"][self.count])
            if np.absolute(self.average_second - self.average_first) > 70:
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("I had an embryo event")
                print("current impedance",self.impedance_current_value)
                print("count", self.count)
                print("time",spreadsheet["TIME"][self.count])
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            self.embryo_reading_counter = 0
            self.embryo_monitoring_bool = False

    def buffer_flush(self):
        self.impedance_buffered_values = []


spreadsheet = pd.read_csv("data_in.csv")

impedance_list = list(filter(lambda name: 'IMPEDANCE' in name, list(spreadsheet)))
print(impedance_list)
impedance_data = [list(spreadsheet[iterator]) for iterator in impedance_list]
serial_impedance = simulation(impedance_data)
impedance_test = well()

while True:
    current_line = serial_impedance.read_value()
    impedance_test.assign_value(current_line[6])
    impedance_test.count += 1