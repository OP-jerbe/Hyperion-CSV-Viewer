# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 07:25:18 2023

@author: Joshua
"""

import tkinter as tk
from tkinter.filedialog import askopenfilenames
import pandas as pd
from typing import TypeVar

pandasDataFrame = TypeVar('pandas.core.frame.DataFrame')

#%% define internal functions


def _fixHeaders(df):
    """Fixes poorly/improperly named headers in hyperion csv file.
    Also converts pressure units from Pascal to mBar if applicable."""
    try: df.rename(columns={'Angular Intensity (mA/str)':'Angular Intensity (mA/sr)'}, inplace=True)
    except: pass
    try: df.rename(columns={'Beam Voltage (kV)':'Beam Voltage (V)'}, inplace=True)
    except: pass
    try: df.rename(columns={'Extractor Voltage (kV)':'Extractor Voltage (V)'}, inplace=True)
    except: pass
    try: df.rename(columns={'Extractor Current (uA)':'Extractor Current (μA)'}, inplace=True)
    except: pass
    try: df.rename(columns={'Beam Supply Current (uA)':'Beam Supply Current (μA)'}, inplace=True)
    except: pass
    try: df.rename(columns={'Lens #1 Current (uA)':'Lens Current (μA)'}, inplace=True)
    except: pass
    try: df.rename(columns={'Lens #1 Voltage (V)':'Lens Voltage (V)'}, inplace=True)
    except: pass
    try: df.rename(columns={'Lens #1 Voltage (kV)':'Lens Voltage (V)'}, inplace=True)
    except: pass
    try:
        df['Source Pressure (Pascal)'] = df['Source Pressure (Pascal)'] * 1e-2 # convert pascals to mbar
        df.rename(columns={'Source Pressure (Pascal)':'Source Pressure (mBar)'}, inplace=True)
    except: pass
    
    return df
    

def _checkForTimeHeader(headers: list) -> bool:
    """Checks that 'Time' is in headers list"""
    boolean = False
    strings = ('Time',)
    for string in strings:
        if string in headers:
            boolean = True
    return boolean
    

#%% Define public functions
def getDataFilepaths() -> tuple:
    """Opens Windows File Explorer to allow user to select the raw test data
    files and returns their paths in a tuple"""
    filepaths = askopenfilenames(title="Choose CSV Files",
                                 #initialdir=r"C:\Users\joshua\Documents\OP Python Scripts\JEOL csv Viewer Project",
                                 filetypes = (("CSV Files","*.csv"),
                                              ("All Files","*.*")))
    return filepaths


def createDataframe(filepaths: tuple) -> pandasDataFrame:
    """Creates a dataframe from the provided filepath to a csv file.
    First it checks that there is a valid filepath. Then it checks that there
    is a column named 'Time'. Then it tries to rename column headers. Then it
    returns the dataframe"""
    if filepaths is not None and filepaths != '':
        df = pd.concat(map(pd.read_csv,filepaths),ignore_index=True)
        headers = df.columns.values.tolist()
        time_header = _checkForTimeHeader(headers) # boolean
        if time_header is True:
            df['Time'] = pd.to_datetime(df['Time'], format='%m/%d/%Y %I:%M:%S %p')
        else:
            tk.messagebox.showerror('Error', 'No column named "Time".')
        df = _fixHeaders(df)
        return df
    else:
        pass


def stripTime(df_headers: list) -> list:
    """Removes the 'Time' column header."""
    if not isinstance(df_headers, list):
        raise TypeError('Argument of stripTime() must be a list')
    time_header = _checkForTimeHeader(df_headers) # boolean
    if time_header is True:
        #df_headers.insert(0, 'None')
        df_headers.remove('Time')
        return df_headers
    else:
        pass




