# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 08:27:25 2023

@author: Joshua
"""

import os
import tkinter as tk
from tkinter.filedialog import asksaveasfilename
from tkinter import ttk
from ttkthemes import ThemedTk
from hyp_csv_cleanup import getDataFilepaths, createDataframe, stripTime
from hyp_csv_plotly import createFig, getTraces, addTraces, updateFigLayout


class App:
    
    def __init__(self, parent):
        
        
        #### initialize root window ####
        self.parent = parent
        self.parent.title('Hyperion csv Viewer')
        self.parent.attributes('-topmost',True)
        self.parent.columnconfigure(0, weight=1)
        self.parent.columnconfigure(1, weight=1)
        self.parent.resizable(False,False)
        
        
        #### Create variables ####
        self.title = tk.StringVar(self.parent)
        self.trace1 = tk.StringVar(self.parent)
        self.trace2 = tk.StringVar(self.parent)
        self.trace3 = tk.StringVar(self.parent)
        self.trace4 = tk.StringVar(self.parent)
        
        self.traces = [self.trace1, self.trace2, self.trace3, self.trace4]
        self.trace_names = [self.trace1.get(), self.trace2.get(), self.trace3.get(), self.trace4.get()]
        
        #### Initialize options for dropdown menus ####
        
        self.df = None
        self.options = ['None']

        #### Create all of the necessary frames ####
        
        # frame to fill the background
        self.background_frame = ttk.Frame(self.parent)
        self.background_frame.pack(expand=True, fill='both')
        
        # frame for plot title label and entry box
        self.frame00 = ttk.Frame(self.background_frame)
        self.frame00.grid(column=0, row=0, columnspan=2, padx=10, pady=5)
        self.frame00['relief'] = 'flat'
        
        # frame for 'Plot 1' label and dropdown box
        self.frame01 = ttk.Frame(self.background_frame)
        self.frame01.grid(column=0, row=1, padx=10, pady=5)
        self.frame01['relief'] = 'flat'
        
        # frame for 'Plot 2' label and dropdown box
        self.frame11 = ttk.Frame(self.background_frame)
        self.frame11.grid(column=1, row=1, padx=10, pady=5)
        self.frame11['relief'] = 'flat'
        
        # frame for 'Plot 3' label and dropdown box
        self.frame02 = ttk.Frame(self.background_frame)
        self.frame02.grid(column=0, row=2, padx=10, pady=5)
        self.frame02['relief'] = 'flat'
        
        # frame for 'Plot 4' label and dropdown box
        self.frame12 = ttk.Frame(self.background_frame)
        self.frame12.grid(column=1, row=2, padx=10, pady=5)
        self.frame12['relief'] = 'flat'
        
        # frame for 'Select csv' button
        self.frame03 = ttk.Frame(self.background_frame)
        self.frame03.grid(column=0, row=3, columnspan=2, padx=10, pady=5)
        self.frame03['relief'] = 'flat'
        
        # frame for 'Plot Data' button
        self.frame04 = ttk.Frame(self.background_frame)
        self.frame04.grid(column=0, row=4, columnspan=2, padx=10, pady=5)
        self.frame04['relief'] = 'flat'
        
        # frame for 'Save Interactive Plot' button
        self.frame05 = ttk.Frame(self.background_frame)
        self.frame05.grid(column=0, row=5, columnspan=2, padx=10, pady=5)
        self.frame05['relief'] = 'flat'
        
        # frame for canvas to display selected CSVs
        self.frame06 = ttk.Frame(self.background_frame)
        self.frame06.grid(column=0, row=6, columnspan=2, padx=10, pady=5)
        self.frame06['relief'] = 'flat'
        
        # subframe for 'Plot 1' dropdown box
        self.dropdown_box_subframe1 = ttk.Frame(self.frame01)
        self.dropdown_box_subframe1.grid(column=0, row=1)
        self.dropdown_box_subframe1['relief'] = 'groove'
        
        # subframe for 'Plot 2' dropdown box
        self.dropdown_box_subframe2 = ttk.Frame(self.frame11)
        self.dropdown_box_subframe2.grid(column=0, row=1)
        self.dropdown_box_subframe2['relief'] = 'groove'
        
        # subframe for 'Plot 3' dropdown box
        self.dropdown_box_subframe3 = ttk.Frame(self.frame02)
        self.dropdown_box_subframe3.grid(column=0, row=1)
        self.dropdown_box_subframe3['relief'] = 'groove'
        
        # subframe for 'Plot 4' dropdown box
        self.dropdown_box_subframe4 = ttk.Frame(self.frame12)
        self.dropdown_box_subframe4.grid(column=0, row=1)
        self.dropdown_box_subframe4['relief'] = 'groove'
        
        
        #### Create all of the label widgets ####
        
        # label for title entry box
        self.title_entry_label = ttk.Label(self.frame00, text='Title:', font=(..., 16, 'bold'))
        self.title_entry_label.grid(column=0, row=0, padx=5, pady=5)
        
        # label for 'Plot 1' dropdown box
        self.plot_option1_label = ttk.Label(self.frame01, text='Plot 1', font=(..., 16, 'bold'))
        self.plot_option1_label.grid(column=0, row=0, pady=2)
        
        # label for 'Plot 2' dropdown box
        self.plot_option2_label = ttk.Label(self.frame11, text='Plot 2', font=(..., 16, 'bold'))
        self.plot_option2_label.grid(column=0, row=0, pady=2)
        
        # label for 'Plot 3' dropdown box
        self.plot_option3_label = ttk.Label(self.frame02, text='Plot 3', font=(..., 16, 'bold'))
        self.plot_option3_label.grid(column=0, row=0, pady=2)
        
        # label for 'Plot 4' dropdown box
        self.plot_option4_label = ttk.Label(self.frame12, text='Plot 4', font=(..., 16, 'bold'))
        self.plot_option4_label.grid(column=0, row=0, pady=2)
        
        
        #### Create the title entry box widget ####
        
        # entry box for plot title
        self.title_entry = ttk.Entry(self.frame00, textvariable=self.title, font=16, width=45)
        self.title_entry.grid(column=1, row=0, padx=5, pady=5)
        
        
        #### Create the dropdown box widgets ####
        
        # option menu for trace1
        self.plot_option1 = ttk.OptionMenu(self.frame01, self.trace1, 'None', *self.options)
        self.plot_option1.grid(column=0, row=1, padx=5, pady=5)
        self.plot_option1.config(width=30)
        
        self.plot_option2 = ttk.OptionMenu(self.frame11, self.trace2, 'None', *self.options)
        self.plot_option2.grid(column=0, row=1, padx=5, pady=5)
        self.plot_option2.config(width=30)
        
        self.plot_option3 = ttk.OptionMenu(self.frame02, self.trace3, 'None', *self.options)
        self.plot_option3.grid(column=0, row=1, padx=5, pady=5)
        self.plot_option3.config(width=30)
        
        self.plot_option4 = ttk.OptionMenu(self.frame12, self.trace4, 'None', *self.options)
        self.plot_option4.grid(column=0, row=1, padx=5, pady=5)
        self.plot_option4.config(width=30)
        
        self.plot_option_menus = (self.plot_option1, self.plot_option2, self.plot_option3, self.plot_option4)
        
        
        #### Create the buttons ####
        
        # button to 'Select CSV'
        self.file_select_button = ttk.Button(self.frame03,
                                            text='Select CSV Files',
                                            width=30,
                                            command=self.file_select_button_action)
        self.file_select_button.pack(padx=5, pady=5, expand=True, fill='both')
        
        # button to 'Plot Data'
        self.plot_fig_button = ttk.Button(self.frame04,
                                         text='Plot Data',
                                         width=30,
                                         command=self.plot_data_button_action)
        self.plot_fig_button.pack(padx=5, pady=5, expand=True, fill='both')
        
        # button to 'Save Interactive Plot'
        self.save_fig_button = ttk.Button(self.frame05,
                                         text='Save Interactive Plot',
                                         width=30,
                                         command=self.save_interactive_plot_action)
        self.save_fig_button.pack(padx=5, pady=5, expand=True, fill='both')
        
        
        #### Create the canvas ####
        
        # canvas for displaying selected csv files
        self.csv_display_canvas = tk.Canvas(self.frame06,
                               background='white',
                               borderwidth=5,
                               relief='ridge',
                               height=200)
        self.csv_display_canvas.pack(padx=5, pady=5)
        self.csv_display_canvas.create_text(60, 20, text='Selected csv files:')
        
        
    def select_csv_files(self):
        """Opens up a filedialog menu to select one or more CSV files,
        creates a dataframe from the csv data, gets the column headers and 
        creates a list of plotting options to add to a drop down menu"""
        self.filepaths = getDataFilepaths()
        if self.filepaths != '':
            self.df = createDataframe(self.filepaths)
            self.column_headers = self.df.columns.values.tolist()
            if 'Time' not in self.column_headers:
                self.filepaths = '' # sets the filepath to empty string so csv_display_canvas doesn't populate with invalid csv file.
            self.options_to_add = stripTime(self.column_headers.copy())
        else:
            self.options = ['None']
            self.options_to_add = []


    #### Change optionmenu items ####
    
    def add_headers_to_options_list(self):
        """Adds column headers (minus 'Time') to the options menu list"""
        if self.options_to_add != self.options[1:] and 'Time' in self.column_headers:
            for option in self.options_to_add:
                self.options.append(option)
            self.options_to_add = [] # reset the list
        else:
            pass

    
    def update_option_menu(self, option_menu):
        """Updates the option menu items to include the headers from the dataframe"""
        option_menu.set_menu('None', *self.options)
    
    def clear_option_menu(self, option_menu):
        """Deletes all options in option menus and sets them to 'None'"""
        option_menu.set_menu('None')
    
    #### Update canvas with csv file names ####
    
    def populate_canvas(self, filepaths):
        """Puts text into canvas frame"""
        x = 20
        y = 40
        for filepath in filepaths:
            self.csv_display_canvas.create_text(x,y, text=os.path.basename(filepath), anchor='nw')
            y = y + 20
    
    def clear_canvas(self):
        """Deletes all text on the canvas."""
        self.csv_display_canvas.delete('all')
        self.csv_display_canvas.create_text(60, 20, text='Selected csv files:')
    
    
    #### Plotly codes ####
    def showFig(self, fig):
        if fig is not None:
            fig.show()
        else:
            pass
    
    def saveFig(self, fig):
        html_filepath = asksaveasfilename(title='Select folder to save HTML file to',
                                          initialdir='.',
                                          filetypes=(("HTML File", "*.html"),("All Files", "*.*")),
                                          defaultextension=".html"
                                          )
        if html_filepath != '' and fig is not None:
            fig.write_html(html_filepath)
            tk.messagebox.showinfo(title='Saved',
                                   message=f'Interactive Plot has been saved to\n{html_filepath}')
    
    
    #### Button actions ####
    def file_select_button_action(self):
        """Functions to execute when 'Select CSV Files' button is pressed."""
        self.select_csv_files()
        self.add_headers_to_options_list()
        self.clear_canvas()
        self.populate_canvas(self.filepaths)
        for option_menu in self.plot_option_menus:
            self.clear_option_menu(option_menu)
            self.update_option_menu(option_menu)

    def plot_data_button_action(self):
        """Functions to execute when 'Plot Data' button is pressed"""
        if self.df is not None:
            self.fig = createFig(self.title.get())
            self.y_traces, self.trace_names = getTraces(self.traces)
            self.fig = addTraces(self.fig, self.df, self.y_traces)
            updateFigLayout(self.fig, self.y_traces, self.trace_names)
            self.showFig(self.fig)
        else:
            tk.messagebox.showinfo(title='No CSV selected', message='Please select csv file.')
        
    def save_interactive_plot_action(self):
        """Functions to execute when 'Save Interactive Plot' button is pressed"""
        try:
            if self.fig is not None:
                self.saveFig(self.fig)
        except:
            pass

root = ThemedTk(theme='plastik')
App(root)
root.mainloop()
    