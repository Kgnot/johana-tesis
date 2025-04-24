from decimal import Decimal
from linecache import getline
import plotly.graph_objects as go
import time


start_time = time.time()



def find_nearest_element(time, start, end):
    print(min(time, key=lambda x: abs(x-Decimal(start))))
    print(time.index(min(time, key=lambda x: abs(x-Decimal(start)))))
    print(min(time, key=lambda x: abs(x-Decimal(end))))
    print(time.index(min(time, key=lambda x: abs(x-Decimal(end)))))
    print((min(time, key=lambda x: abs(x-Decimal(1.840)))+min(time, key=lambda x: abs(x-Decimal(0.600))))/2)
    print(time.index(min(time, key=lambda x: abs(x-(min(time, key=lambda x: abs(x-Decimal(end)))+min(time, key=lambda x: abs(x-Decimal(start))))/2))))

def judge_line_number(path):
    count = 1
    f = open(path,"r")
    line = f.readline()
    while line!="":
        s=line[:4]
        if s.upper()=="time".upper():
          return count
        else:
          count = count + 1
          line = f.readline()

def generate_dict(path):
    def sto_Getline(path):
      return getline(path, judge_line_number(path)).strip('\n').split()
    for each in dict(zip(sto_Getline(path), range(0,len(sto_Getline(path))))):
      print(each, ':', dict(zip(sto_Getline(path), range(0,len(sto_Getline(path)))))[each])

def three(fig, y1, y1_name, y2, y2_name, y3, y3_name, title):
    fig.add_trace(go.Scatter(x=time_5, y=y1, name=y1_name, mode="lines",
                         line=dict(color='red', width=0.5, dash='solid')))
    fig.add_trace(go.Scatter(x=time_10, y=y2, name=y2_name, mode="lines",
                         line=dict(color='blue', width=0.5, dash='solid')))
    fig.add_trace(go.Scatter(x=time_20, y=y3, name=y3_name, mode="lines",
                         line=dict(color='green', width=0.5, dash='solid')))
    fig.update_layout(title='<b>'+title+'<b>', xaxis_title='time', yaxis_title='value',font=dict(
        family="Courier New, monospace",
        size=24,
        #color="RebeccaPurple"
    ))
    fig.show()

def four(fig, x, y1, y1_name, y2, y2_name, y3, y3_name, y4, y4_name, title, fig_name):
    fig.add_trace(go.Scatter(x=x, y=y1, name=y1_name, mode="lines",
                         line=dict(color='black', width=2, dash='solid')))
    fig.add_trace(go.Scatter(x=x, y=y2, name=y2_name, mode="lines",
                         line=dict(color='grey', width=2, dash='solid')))
    fig.add_trace(go.Scatter(x=x, y=y3, name=y3_name, mode="lines",
                         line=dict(color='black', width=2, dash='dash')))
    fig.add_trace(go.Scatter(x=x, y=y4, name=y4_name, mode="lines",
                         line = dict(color='grey', width=2, dash='dash')))
    fig.update_layout(title={
    'text': '<b>'+title+'<b>',
    'y': 0.9,
    'x': 0.5,
    'xanchor': 'center',
    'yanchor': 'top'}, xaxis_title='time', yaxis_title='value',font=dict(
        family="Courier New, monospace",
        size=24), template="simple_white"
        )


r_FO = 1.43 #@param {type:"number"}

def four_IDTool(fig, x, y1, y1_name, y2, y2_name, y3, y3_name, y4, y4_name, title, fig_name):
    fig.add_trace(go.Scatter(x=x, y=y1, name=y1_name, mode="lines",
                         line=dict(color='black', width=2, dash='solid')))
    fig.add_trace(go.Scatter(x=x, y=y2, name=y2_name, mode="lines",
                         line=dict(color='grey', width=2, dash='solid')))
    fig.add_trace(go.Scatter(x=x, y=y3, name=y3_name, mode="lines",
                         line=dict(color='black', width=2, dash='dash')))
    fig.add_trace(go.Scatter(x=x, y=y4, name=y4_name, mode="lines",
                         line = dict(color='grey', width=2, dash='dash')))
    fig.add_vline(x=r_FO, annotation_position="top",annotation_text="r_FO", line_width=2, line_dash="dash", line_color="red")
    #fig.add_vline(x=0.308, annotation_position="bottom",annotation_text="l_FO", line_width=1, line_dash="dash", line_color="blue")
    #fig.add_vline(x=0.888, annotation_position="top",annotation_text="l-FS", line_width=1, line_dash="dash", line_color="red")
    #fig.add_vline(x=0.918, annotation_position="bottom",annotation_text="r_FO", line_width=1, line_dash="dash", line_color="blue")
    fig.update_layout(title={
    'text': '<b>'+title+'<b>',
    'y': 0.95,
    'x': 0.5,
    'xanchor': 'center',
    'yanchor': 'top'}, yaxis_title='value',font=dict(
        family="Courier New, monospace",
        size=24), template="simple_white"
        )

def six(fig, x, y1, y1_name, y2, y2_name, y3, y3_name, y4, y4_name, y5, y5_name, y6, y6_name, title, fig_name):
    fig.add_trace(go.Scatter(x=x, y=y1, name=y1_name, mode="lines",
                            line=dict(color='black', width=2, dash='solid')))
    fig.add_trace(go.Scatter(x=x, y=y2, name=y2_name, mode="lines",
                            line=dict(color='grey', width=2, dash='solid')))
    fig.add_trace(go.Scatter(x=x, y=y3, name=y3_name, mode="lines",
                            line=dict(color='black', width=2, dash='solid')))
    fig.add_trace(go.Scatter(x=x, y=y4, name=y4_name, mode="lines",
                            line = dict(color='grey', width=2, dash='solid')))
    fig.add_trace(go.Scatter(x=x, y=y5, name=y5_name, mode="lines",
                            line=dict(color='black', width=2, dash='solid')))
    fig.add_trace(go.Scatter(x=x, y=y6, name=y6_name, mode="lines",
                            line = dict(color='grey', width=2, dash='solid')))
    fig.update_layout(title='<b>'+title+'<b>', xaxis_title='time', yaxis_title='value',font=dict(
        family="Courier New, monospace",
        size=24,
        #color="RebeccaPurple"
    ))
    fig.show()
    fig.write_image(fig_name)


print('finished')