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

    # Simulating arduino output
    def read_value(self):
        #time.sleep(.001)
        if (self.num_values_emitted < len(self.values[0])):
            self.num_values_emitted = self.num_values_emitted + 1
            return [place_holder[self.num_values_emitted - 1] for place_holder in self.values]
        else:
            return []
#well classes
# class all_wells:
#     def __init__(self):
#         self.dict = {}
#     def well_dictionary(self, list):
#         self.dict = {
#         for x in range(len(list)):
#             x: str(list[x])
#     }
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
        self.output_embryo = 0

    def impedance_assign_value(self, argument_value):
        #This filters the data for when air is in the lines, need to come up with some better filter check for air
        #at a later date
            #pass in the current impedance and create a buffer of size 5 of the most recent impedance values
            self.impedance_current_value = argument_value
            if len(self.impedance_buffered_values) < self.buffer_size:
                self.impedance_buffered_values.append(argument_value)
                self.impedance_count += 1
            self.impedance_buffered_values = self.impedance_buffered_values[1:]
            self.impedance_buffered_values.append(argument_value)
            self.impedance_count += 1

    def has_event(self):
        if(self.impedance_current_value < 100000 and self.impedance_current_value != 0):
            if (np.absolute(self.impedance_buffered_values[-1] - self.impedance_buffered_values[
                0]) > 75 and self.embryo_monitoring_bool != True):
                self.average_first = sum(self.impedance_buffered_values) / len(self.impedance_buffered_values)
                # print("first average values", self.impedance_buffered_values)
                # print("first average", self.average_first)
                self.buffer_flush()
                self.embryo_monitoring_bool = True
            if self.embryo_monitoring_bool == True:
                self.embryo_reading_counter += 1
            if (self.embryo_reading_counter == 6):
                # print("second average values", self.impedance_buffered_values)
                self.average_second = sum(self.impedance_buffered_values) / len(self.impedance_buffered_values)
                # print("second average", self.average_second)
                # print("average difference", np.absolute(self.average_second - self.average_first))
                # print("time", spreadsheet["TIME"][self.count])
                result = np.absolute(self.average_second - self.average_first)
                print(result)
                if result > 70:
                    pass
                    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    # print("I had an embryo event")
                    # print("current impedance",self.impedance_current_value)
                    # print("count", self.count)
                    # print("time",spreadsheet["TIME"][self.count])
                    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                self.embryo_reading_counter = 0
                self.embryo_monitoring_bool = False

    def buffer_flush(self):
        self.impedance_buffered_values = []

spreadsheet = pd.read_csv("data_in2.csv")

impedance_list = list(filter(lambda name: 'IMPEDANCE' in name, list(spreadsheet)))
impedance_data = [list(spreadsheet[iterator]) for iterator in impedance_list]
serial_impedance = simulation(impedance_data)
instancelist = [well() for i in range(len(impedance_list))]
data_array = [impedance_list]

for i in range(len(spreadsheet["TIME"]) - 100):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Simulation placeholder
    current_line = serial_impedance.read_value()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    data_temp = []
    for i in range(len(impedance_list)):
        instancelist[i].impedance_assign_value(current_line[i])
        print(instancelist[i].impedance_buffered_values)
        instancelist[i].has_event()
        instancelist[i].count += 1
        data_temp.append(instancelist[i].impedance_current_value)
    data_array.append(data_temp)
print(data_array)
data_frame_values = pd.DataFrame(data_array)
export_csv = data_frame_values.to_csv (r'C:\Users\matts\PycharmProjects\embryo_class\export_dataframe.csv', index = None, header=True) #Don't forget to add '.csv' at the end of the path

# current_row = pd.DataFrame(current_line)
# logged_values.append(current_row)
# print(logged_values)
# print(logged_values)
























































# Cars = {'Brand': ['Honda Civic','Toyota Corolla','Ford Focus','Audi A4'],
#         'Price': [22000,25000,27000,35000]
#         }
# df = DataFrame(Cars, columns= ['Brand', 'Price'])
# export_csv = df.to_csv (r'C:\Users\matts\PycharmProjects\embryo_class\export_dataframe.csv', index = None, header=True) #Don't forget to add '.csv' at the end of the path
# print (df)
#export_csv = logged_values.to_csv (r'C:\Users\matts\PycharmProjects\embryo_class\export_dataframe.csv', index = None, header=True) #Don't forget to add '.csv' at the end of the path
#print (logged_values)
#class pandas.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)