from importlib.resources import path
import tkinter as tk
from tkinter import filedialog as fd

from pyparsing import col
from audio import Audio
from devices import Devices
import sounddevice as sd 
import numpy as np
import pandas as pd
import os

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Re-Record')
        self.root.iconbitmap('icon.ico')
        
        # create container
        top_frame = tk.LabelFrame(self.root,text='Device Settings', width=690, height=100)
        center_frame = tk.Frame(self.root, width=700, height=450)

        top_frame.grid(row=0, sticky='ew', padx=1)
        center_frame.grid(row=1,sticky='nsew')

        center_left_frame = tk.LabelFrame(center_frame, text='Waiting', width=545, height=400)
        center_right_frame = tk.LabelFrame(center_frame, text='Record', width=150, height=400)


        center_left_frame.grid(row=0, column=0,padx=1)
        center_right_frame.grid(row=0, column=1)

        top_frame.grid_propagate(0)
        center_left_frame.grid_propagate(0)
        center_right_frame.grid_propagate(0)

        # create Device GUI
        self.devices = Devices()
        input_label = tk.Label(top_frame, text='Input Device :')
        output_label = tk.Label(top_frame, text='Output Device :')
        input_devices_name = self.devices.available_input_devices.iloc[1:].name
        input_device_var = tk.StringVar(self.root)
        input_device_var.set(input_devices_name.loc[self.devices.selected_input_index])
        input_option = tk.OptionMenu(top_frame, input_device_var, *input_devices_name.tolist())
        input_option.config(width=30)

        output_devices_name = self.devices.available_output_devices.iloc[1:].name
        output_device_var = tk.StringVar(self.root)
        output_device_var.set(output_devices_name.loc[self.devices.selected_output_index])
        output_option = tk.OptionMenu(top_frame, output_device_var, *output_devices_name.tolist())
        output_option.config(width=30)

        frame2 = tk.Frame(top_frame)
        frame2.grid(row=1, column=3, sticky='ew', pady=10)

        def cancel():
            output_device_var.set(output_devices_name.loc[self.devices.selected_output_index])
            input_device_var.set(input_devices_name.loc[self.devices.selected_input_index])

        def refresh():
            self.devices.refreshSetting()
            cancel()

        def save():
            input_idx = int(self.devices.available_devices[self.devices.available_devices['name'] == input_device_var.get()].index[0])
            output_idx = int(self.devices.available_devices[self.devices.available_devices['name'] == output_device_var.get()].index[0])
            self.devices.changeInputDevices(input_idx)
            self.devices.changeOutputDevices(output_idx)

        save_btn = tk.Button(frame2, text='save', command=save)
        save_btn.config(width=10)
        cancel_btn = tk.Button(frame2, text='cancel', command=cancel)
        cancel_btn.config(width=10)
        refresh_btn = tk.Button(top_frame,text='refresh', command=refresh)
        refresh_btn.config(width=8)

        input_label.grid(row=0, column=0, padx=15)
        input_option.grid(row=0, column=1)
        output_label.grid(row=0, column=2, padx=15)
        output_option.grid(row=0, column=3)
        save_btn.grid(column=0, row=0)
        cancel_btn.grid(column=1, row=0, padx=20)
        refresh_btn.grid(column=0, row=1)

        # create Center Left GUI
        frame3 = tk.Frame(center_left_frame)
        frame3.config(width=540, height=30)
        listBox = tk.Listbox(center_left_frame)
        listBox.config(width=88, height=21)
        listBox.grid(row=1,column=0, padx=5, pady=5)
        frame3.grid(row=0, column=0, sticky='w')
        frame3.grid_propagate(0)

        def setformatPath(path):
            return path.replace('\\', '/')

        def browsePath():
            path = fd.askdirectory()
            self.save_path.set(path)

        save_to = tk.Label(frame3, text='save to :')
        self.save_path = tk.StringVar(value=(setformatPath(os.getcwd()) + '/record'))
        save_path_input = tk.Entry(frame3, textvariable=self.save_path)
        browse = tk.Button(frame3, text='Browse', command=browsePath)

        browse.config(width=10)
        save_path_input.config(width=62)

        save_to.grid(row=0, column=0, pady=4, padx=1)
        save_path_input.grid(row=0, column=1)
        browse.grid(row=0, column=2, padx=10)

        # create Audio GUI
        self.audio = Audio()
        self.cancelID = ''
        def selectFile():
            paths = np.array(fd.askopenfilenames())
            listBox.insert('end', *paths)
            path = listBox.get(0)
            self.audio.loadFile(path)

        def stopAudio():
            self.audio.stopAudio()
            auto_var.set(0)
            self.root.after_cancel(self.cancelID)

        def afterPlay():
            self.audio.saveFile(setformatPath(self.save_path.get()))
            listBox.delete(0)
            path = listBox.get(0)
            if( auto_var.get() and (path != '')):
                self.audio.loadFile(path)
                self.audio.palyAndRec()
                self.cancelID = self.root.after(self.audio.time * 1000, afterPlay)

        def playAndRec():
            path = listBox.get(0)
            if(path == ''):
                return 
            self.audio.loadFile(path)
            self.audio.palyAndRec()
            self.cancelID = self.root.after(self.audio.time * 1000, afterPlay)

        select_btn = tk.Button(center_right_frame, text='Select Files', command=selectFile)
        play_btn = tk.Button(center_right_frame, text='Play & Record', command=playAndRec)
        stop_btn = tk.Button(center_right_frame, text='Stop', command=stopAudio)
        frame4 = tk.Frame(center_right_frame)
        auto_var = tk.IntVar()
        auto_check = tk.Checkbutton(frame4, text='Auto', variable=auto_var, onvalue=1, offvalue=0)

        select_btn.config(width=12)
        play_btn.config(width=12)
        stop_btn.config(width=12)

        select_btn.grid(row=0, padx = 30, pady=20)
        play_btn.grid(row=1)
        frame4.grid(row=2,sticky='w', padx = 30, pady=5)
        stop_btn.grid(row=3)
        auto_check.grid(row=0)



        self.root.geometry('700x500')
        self.root.mainloop()

# GUI()


# root = tk.Tk()
# root.title("Re-record")
# root.iconbitmap('icon.ico')

# # create container
# top_frame = tk.LabelFrame(root,text='Device Settings', width=690, height=100)
# center_frame = tk.Frame(root, width=700, height=450)

# top_frame.grid(row=0, sticky='ew', padx=1)
# center_frame.grid(row=1,sticky='nsew')

# center_left_frame = tk.LabelFrame(center_frame, text='Waiting', width=545, height=400)
# center_right_frame = tk.LabelFrame(center_frame, text='Record', width=150, height=400)


# center_left_frame.grid(row=0, column=0,padx=1)
# center_right_frame.grid(row=0, column=1)

# top_frame.grid_propagate(0)
# center_left_frame.grid_propagate(0)
# center_right_frame.grid_propagate(0)

# # create Device GUI
# devices = Devices()
# input_label = tk.Label(top_frame, text='Input Device :')
# output_label = tk.Label(top_frame, text='Output Device :')
# input_devices_name = devices.available_input_devices.iloc[1:].name
# input_device_var = tk.StringVar(root)
# input_device_var.set(input_devices_name.loc[devices.selected_input_index])
# input_option = tk.OptionMenu(top_frame, input_device_var, *input_devices_name.tolist())
# input_option.config(width=30)

# output_devices_name = devices.available_output_devices.iloc[1:].name
# output_device_var = tk.StringVar(root)
# output_device_var.set(output_devices_name.loc[devices.selected_output_index])
# output_option = tk.OptionMenu(top_frame, output_device_var, *output_devices_name.tolist())
# output_option.config(width=30)

# frame2 = tk.Frame(top_frame)
# frame2.grid(row=1, column=3, sticky='ew', pady=10)

# def cancel():
#     output_device_var.set(output_devices_name.loc[devices.selected_output_index])
#     input_device_var.set(input_devices_name.loc[devices.selected_input_index])

# def refresh():
#     devices.refreshSetting()
#     cancel()

# def save():
#     input_idx = int(devices.available_devices[devices.available_devices['name'] == input_device_var.get()].index[0])
#     output_idx = int(devices.available_devices[devices.available_devices['name'] == output_device_var.get()].index[0])
#     devices.changeInputDevices(input_idx)
#     devices.changeOutputDevices(output_idx)

# save_btn = tk.Button(frame2, text='save', command=save)
# save_btn.config(width=10)
# cancel_btn = tk.Button(frame2, text='cancel', command=cancel)
# cancel_btn.config(width=10)
# refresh_btn = tk.Button(top_frame,text='refresh', command=refresh)
# refresh_btn.config(width=8)

# input_label.grid(row=0, column=0, padx=15)
# input_option.grid(row=0, column=1)
# output_label.grid(row=0, column=2, padx=15)
# output_option.grid(row=0, column=3)
# save_btn.grid(column=0, row=0)
# cancel_btn.grid(column=1, row=0, padx=20)
# refresh_btn.grid(column=0, row=1)

# # create Center Left GUI
# frame3 = tk.Frame(center_left_frame)
# frame3.config(width=540, height=30)
# listBox = tk.Listbox(center_left_frame)
# listBox.config(width=88, height=21)
# listBox.grid(row=1,column=0, padx=5, pady=5)
# frame3.grid(row=0, column=0, sticky='w')
# frame3.grid_propagate(0)

# def setformatPath(path):
#     return path.replace('\\', '/')

# def browsePath():
#     path = fd.askdirectory()
#     save_path.set(path)

# save_to = tk.Label(frame3, text='save to :')
# save_path = tk.StringVar(value=(setformatPath(os.getcwd()) + '/record'))
# save_path_input = tk.Entry(frame3, textvariable=save_path)
# browse = tk.Button(frame3, text='Browse', command=browsePath)

# browse.config(width=10)
# save_path_input.config(width=62)

# save_to.grid(row=0, column=0, pady=4, padx=1)
# save_path_input.grid(row=0, column=1)
# browse.grid(row=0, column=2, padx=10)

# # create Audio GUI
# audio = Audio()
# cancelID = ''
# def selectFile():
#     paths = np.array(fd.askopenfilenames())
#     listBox.insert('end', *paths)
#     path = listBox.get(0)
#     audio.loadFile(path)

# def stopAudio():
#     audio.stopAudio()
#     auto_var.set(0)
#     root.after_cancel(cancelID)

# def afterPlay():
#     audio.saveFile(setformatPath(save_path.get()))
#     listBox.delete(0)
#     path = listBox.get(0)
#     if( auto_var.get() and (path != '')):
#         audio.loadFile(path)
#         audio.palyAndRec()
#         cancelID = root.after(audio.time * 1000, afterPlay)

# def playAndRec():
#     path = listBox.get(0)
#     if(path == ''):
#         return 
#     audio.loadFile(path)
#     audio.palyAndRec()
#     cancelID = root.after(audio.time * 1000, afterPlay)

# select_btn = tk.Button(center_right_frame, text='Select Files', command=selectFile)
# play_btn = tk.Button(center_right_frame, text='Play & Record', command=playAndRec)
# stop_btn = tk.Button(center_right_frame, text='Stop', command=stopAudio)
# frame4 = tk.Frame(center_right_frame)
# auto_var = tk.IntVar()
# auto_check = tk.Checkbutton(frame4, text='Auto', variable=auto_var, onvalue=1, offvalue=0)

# select_btn.config(width=12)
# play_btn.config(width=12)
# stop_btn.config(width=12)

# select_btn.grid(row=0, padx = 30, pady=20)
# play_btn.grid(row=1)
# frame4.grid(row=2,sticky='w', padx = 30, pady=5)
# stop_btn.grid(row=3)
# auto_check.grid(row=0)



# root.geometry('700x500')
# root.mainloop()