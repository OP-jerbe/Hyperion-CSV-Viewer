# -*- coding: utf-8 -*-
"""
Created on Tue May  2 06:28:47 2023

@author: Joshua
"""
import tkinter as tk
import plotly.io as pio
import plotly.graph_objects as go

pio.renderers.default='browser'

def createFig(plot_title: str):
    """Creates the plotly figure and applies standard formatting."""
    fig = go.Figure()
    fig.update_layout(
        paper_bgcolor='rgba(132,132,132,1)',
        plot_bgcolor='black',
        legend_font_color='black',
        title=dict(text=plot_title, font=dict(size=28), x=0.5),
        
        legend=dict(
            orientation='h',
            xanchor='center',
            x=0.5,  # value must be between 0 to 1.
        ),
        
        xaxis=dict(
            domain=[0, 1],
            showgrid=False,
            color='black'
        ),
    )
    return fig


def addTraces(fig, df, trace_names:list):
    """Adds the traces in traces list to the figure"""
    if 'None' not in trace_names:
        for traceName_axisName_color in zip(trace_names,yaxis_names,trace_colors):
            fig.add_trace(go.Scatter(
                x=df['Time'],
                y=df[traceName_axisName_color[0]], # trace data
                name=traceName_axisName_color[0], # trace name (one of the column headers)
                yaxis=traceName_axisName_color[1], # yaxis name (y1, y2, y3, or y4)
                line=dict(color=traceName_axisName_color[2]) # trace color
            ))
        return fig
    else:
        pass


def updateFigLayout(fig, y_traces:list, Y_TRACES:list):
    """Updates the figure layout"""
    # y_traces is a list of strings of all 4 selections from the dropdown menu, including 'None's
    # Y_TRACES is a list of strings of just the non-'None' dropdown menu selections
    if 'None' not in y_traces:
        yaxes_layouts = [
            dict( # y1 = right side, left column
                title=Y_TRACES[0],
                side='right',
                exponentformat='E',
                color = trace_colors[0],
                showgrid=False,
                zeroline=False
            ),
            
            dict( # y2 = right side, right column
                title=Y_TRACES[1],
                anchor='free',
                overlaying='y',
                autoshift=True,
                side='right',
                exponentformat='E',
                color = trace_colors[1],
                showgrid=False,
                zeroline=False
            ),
            
            dict( # y3 = left side, right column
                title=Y_TRACES[2],
                exponentformat='E',
                overlaying='y',
                color = trace_colors[2],
                showgrid=False,
                zeroline=False
            ),
            
            dict( # y4 = left side, left column
                title=Y_TRACES[3],
                anchor='free',
                overlaying='y',
                autoshift=True,
                side='left',
                exponentformat='E',
                color = trace_colors[3],
                showgrid=False,
                zeroline=False
            ),
        ]
        
        xaxis_layout = [
            dict(
                title = 'Time',
                #exponentformat='E'
                )
        ]
    
        fig.update_layout( 
            yaxis1=yaxes_layouts[0],
            yaxis2=yaxes_layouts[1],
            yaxis3=yaxes_layouts[2],
            yaxis4=yaxes_layouts[3],
            xaxis=xaxis_layout[0]
        )
    
        return fig
    else:
        pass
    
def getTraces(y_traces:list): # y_traces is a list of tkinter variables
    """This function gets the list of traces for the drop down menu selections"""
    trace_names = []
    Y_TRACES = []
    for trace in y_traces:
        trace_names.append(trace.get())
        Y_TRACES.append(trace.get())
    YAXIS_NAMES = yaxis_names.copy()
    TRACE_COLORS = trace_colors.copy()
    if 'None' in Y_TRACES:
        none_idx = sorted(list_duplicates_of(Y_TRACES,'None'), reverse=True)
        if 0 in none_idx and len(none_idx) != 4: # check that zero is not in none_idx
            errorMessage2()
        elif len(none_idx) != 4: # check that none_idx does not have a length of 4
            for indx in none_idx:
                if indx < len(Y_TRACES):
                    Y_TRACES.pop(indx)
                    YAXIS_NAMES.pop(indx)
                    TRACE_COLORS.pop(indx)
            #print(f'Y_TRACES = {Y_TRACES}')
        else:
            errorMessage3()
    return Y_TRACES, trace_names

def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs

def errorMessage2():
    """Create an error message window telling the user to choose Plot 1 data"""
    tk.messagebox.showerror('Error', 'Please choose Plot 1 data.')
    #plot_selection_window.attributes('-topmost',True)

def errorMessage3():
    """Create an error message window telling the user to choose at least one variable to plot"""
    tk.messagebox.showerror('Error', 'Please choose data to plot.')
    #plot_selection_window.attributes('-topmost',True)

yaxis_names = ['y1', 'y2', 'y3', 'y4']
trace_colors = ['red', 'white', 'limegreen', 'yellow']