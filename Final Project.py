#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 12:58:16 2019

@author: florian
"""

import dash
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_table
import pandas as pd
from collections import OrderedDict
from joblib import Parallel, delayed

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import math
import datetime as dt




rho=0.6
kappa=1.0
theta=0.1
lamb=0
sigma=0.1
vt=0.1


sigma_r=0.02
theta_r=0.05
k_r=0.20


#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################
#Dash Part

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': 'white',
    'text': '#7FDBFF',
    'background2':'white'
}

df = pd.DataFrame(OrderedDict([
    ('Parameters', ['Amount', 'Currency', 'Rate']),
    ('Values', [0,'Eur',0]),
]))

df_per_row_dropdown = pd.DataFrame(OrderedDict([
    ('Parameters', ['Call', 'Put', 'Call Strike','Put Strike','Maturity']),
    ('Values', [0,0,0,0,0]),
]))

app.layout = html.Div(children=[
    html.Div([html.Tr([
        html.H1(['Option Pricing'],
        style={'fontSize':50}),html.Td([html.Img(src='https://www.master203.com/images/layout/logo.png')],style={'padding-left': '500px','padding-bottom':'30px','border':'1px rgb(10,186,181) solid'})]),
        
        html.Label('Antoine Le Tacon,   Léa Pinto,    Florian Schirrer')
                    ], 
            style={
            'textAlign': 'left',
            'backgroundColor': 'rgb(10,186,181)',
            'color':'white',
            'height':150,
            'padding-bottom':'10px'
        }),




 html.Div([
        html.Div(['General Parameters']),
                
                    ], 
            style={
            'textAlign': 'left',
            'backgroundColor': 'rgb(0,32,96)',
            'color':'white',
            'margin-top':'20px',
            'height':30,
            'fontSize':20
        }),


html.Table(style={
        #'border':'1px black solid',
        'margin-top':'20px',
        'bold':'2px',
        'border-top':'2px black solid',
        'border-bottom':'2px black solid',
        'width':'1305px'
        
        },
    children=[
    
    html.Tr([html.Label(''),html.Td([html.Label('Amount')],style={'border':'1px white solid','padding-left': '300px'}),html.Td([html.Label('Strike (%)')],style={'border':'1px white solid','padding-right': '150px'})
    ,html.Td([html.Label('Buy & Sell')],style={'border':'1px white solid','padding-left': '50px'})]),
    html.Tr([html.Label('Call'),
    html.Td([dcc.Input(id='number_call', type='number',placeholder=0, min=0, n_blur_timestamp=1,value=1,style={'margin-left':'250px','width': 120})],style={'border':'1px white solid'}),
    html.Td([dcc.Input(id='Strike_call', type='number',placeholder=100, min=0, value=100,style={'margin-left':'-20px','width': 120})],style={'border':'1px white solid'}),
    html.Td([dcc.Dropdown(id='Buy_Sell_call',
            options=[
            {'label': 'Buy', 'value': 'Buy'},
            {'label': 'Sell', 'value': 'Sell'}
            ],
        style={'width': 120, 'fontSize':12,'border-spacing':'1px','padding':'1px'},
        value='Buy')],style={'border':'1px white solid'})
    ]),
    
    html.Tr([html.Label('Put'),
    html.Td([dcc.Input(id='number_put', type='number',placeholder=0, min=0, value=1,style={'margin-left':'250px','width': 120})]),
    html.Td([dcc.Input(id='Strike_put', type='number',placeholder=100, min=0, value=100,style={'margin-left':'-20px','width': 120})]),
    html.Td([dcc.Dropdown(id='Buy_Sell_put',
            options=[
            {'label': 'Buy', 'value': 'Buy'},
            {'label': 'Sell', 'value': 'Sell'}
            ],
        style={'width': 120, 'fontSize':12,'border-spacing':'1px','padding':'1px'},
        value='Buy')])
    ])]),

html.Div([
        html.Tr(['Market Parameters',html.Td([''])]),
                
                    ], 
            style={
            'textAlign': 'left',
            'backgroundColor': 'rgb(0,32,96)',
            'color':'white',
            'margin-top':'20px',
            'height':30,
            'fontSize':20,
            'width':'500px'
        }),

html.Table(style={
        #'border':'1px black solid',
        'margin-top':'20px',
        'border-top':'2px black solid',
        'border-bottom':'2px black solid',
        'width':'500px'
        
        },children=[
    
    html.Tr([html.Label('Underlying'),
    html.Td([dcc.Dropdown(
        id='Underlying_dropdown',
        placeholder='SX5E',
        options=[
            {'label': 'SX5E', 'value': 'SX5E'},
            {'label': 'SPX', 'value': 'SPX'},
            {'label': 'NIKKEI', 'value': 'NIKKEI'}
        ],
        style={'width': 120, 'fontSize':12,'margin-left':'105px'},
        value='SX5E'
    )],style={'border':'1px white solid'})]),

html.Tr([html.Label('Initial Spot (%)'),
    html.Td([dcc.Input(id='Spot', type='number',placeholder=0, min=0, value=100,style={'width': 120,'margin-left':'210px'})],style={'border':'1px white solid'})]),

html.Tr([html.Label('Rates'),
    html.Td([dcc.Dropdown(
        id='Rates_dropdown',
        options=[
            {'label': 'Euribor 3M', 'value': 'Euribor 3M'},
            {'label': 'Libor 3M USD', 'value': 'Libor 3M USD'}
        ],
        style={'width': 120, 'fontSize':12,'margin-left':'105px'},
        value='Euribor 3M'
    )],style={'border':'1px white solid'})]),


    html.Tr([html.Label('Maturity'),
    html.Td([dcc.Input(id='Maturity', type='number',value=1, min=0, step=1,style={'width': 120,'margin-left':'210px'})],style={'border':'1px white solid'})]),

    html.Br(),
    
    #html.Button('Price', id='button'),
    #html.Div(id='body-div'),


    ]),

html.Div([
        html.Tr(['Simulation Parameters']),
                
                    ], 
            style={
            'textAlign': 'left',
            'backgroundColor': 'rgb(0,32,96)',
            'color':'white',
            'margin-top':'20px',
            'height':30,
            'fontSize':20,
            'width':'500px'
        }),

html.Table(style={
        #'border':'1px black solid',
        'margin-top':'20px',
        'bold':'2px',
        'border-top':'2px black solid',
        'border-bottom':'2px black solid',
        'width':'500px'
        
        },
    children=[
    html.Tr([html.Label('Number of Simulations'),
    html.Td([dcc.Input(id='number_sim', type='number',placeholder=0, min=0, n_blur_timestamp=1,value=1000,style={'margin-left':'90px','width': 110})],style={'border':'1px white solid'})]),
    html.Tr([html.Label('Number of Paths'),
    html.Td([dcc.Input(id='number_paths', type='number',placeholder=0, min=0, n_blur_timestamp=1,value=365,style={'margin-left':'90px','width': 110})])
    ])]),




 html.Tr(children=[html.Button('Price', id='button',style={'margin-top':'20px'}),html.Td(id='body-div',
             style={'width': 120, 'fontSize':23,'color':'rgb(0,32,96)','border':'1px white solid','padding-left': '230px'})
            ]),

html.Div([dcc.Graph(
        id='graph',
        config={
            'showSendToCloud': True,
            'plotlyServerURL': 'https://plot.ly'
        }
    )],style={'margin-left':'550px','width':'55%','margin-top':'-550px'}),

    html.Div([dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
    dcc.Tab(label='Heston Model Graphic', value='tab-1-example'),
    dcc.Tab(label='Vasicek Model Graphic', value='Rate_Tab'),
    dcc.Tab(label='Underlying Graphic', value='Underlying_Tab'),
    ])],style={'margin-top':'200px'}),
    html.Div(id='tabs-content-example')
])

#########################################################################################################################################################
#########################################################################################################################################################
#########################################################################################################################################################



@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('number_call', 'value'),
     dash.dependencies.Input('Strike_call', 'value'),
     dash.dependencies.Input('Buy_Sell_call', 'value'),
     dash.dependencies.Input('number_put', 'value'),
     dash.dependencies.Input('Strike_put', 'value'),
     dash.dependencies.Input('Buy_Sell_put', 'value'),
    ])


#Graphic of the payoff to illustrate the options strategy princing by the user
def update_output(number_call,Strike_call,Buy_Sell_call,number_put,Strike_put,Buy_Sell_put):

    #Graphic of the payoff to illustrate the options strategy princing by the user
    if number_call==None:
        number_call=0
    if Strike_call==None:
        Strike_call=0
    if Buy_Sell_call==None:
        Buy_Sell_call=0
        
    if number_put==None:
        Buy_Sell_call=0
    if Strike_put==None:
        Buy_Sell_call=0
    if Buy_Sell_put==None:
        Buy_Sell_call=0
    
    
    x_call_put=np.zeros(200)
    y_call_put=np.zeros(200)
    St=np.zeros(200)

        
    for i in range(200):
        St[i]=i
        

        if Buy_Sell_call=='Buy'and Buy_Sell_put=='Buy':
            for i in range(200):
                y_call_put[i]=number_call*max(St[i]-Strike_call,0)+number_put*max(Strike_put-St[i],0)
                x_call_put[i]=St[i]
                
        elif Buy_Sell_call=='Sell'and Buy_Sell_put=='Sell':
            for i in range(200):
                y_call_put[i]=number_call*min(Strike_call-St[i],0)+number_put*min(St[i]-Strike_put,0)
                x_call_put[i]=St[i]
                
        elif Buy_Sell_call=='Buy'and Buy_Sell_put=='Sell':
            for i in range(200):
                y_call_put[i]=number_call*max(St[i]-Strike_call,0)+number_put*min(St[i]-Strike_put,0)
                x_call_put[i]=St[i]
                
        elif Buy_Sell_call=='Sell'and Buy_Sell_put=='Buy':
            for i in range(200):
                y_call_put[i]=number_call*min(Strike_call-St[i],0)+number_put*max(Strike_put-St[i],0)
                x_call_put[i]=St[i]
                

    return {
        'data': [{
            'type': 'scatter',
            'x': x_call_put,
            'y':y_call_put,
            'color':'red'
        }],
        'layout': {
            'title': 'Payoff Strategy',
            'xaxis':{'title':'Underlying'}
        }
    }


@app.callback(
    [Output(component_id='body-div', component_property='children'),Output('tabs-content-example', 'children')],
    [Input(component_id='button', component_property='n_clicks'),
     dash.dependencies.Input('number_call', 'value'),
     dash.dependencies.Input('Strike_call', 'value'),
     dash.dependencies.Input('Buy_Sell_call', 'value'),
     dash.dependencies.Input('number_put', 'value'),
     dash.dependencies.Input('Strike_put', 'value'),
     dash.dependencies.Input('Buy_Sell_put', 'value'),
     dash.dependencies.Input('Maturity', 'value'),
     Input('tabs-example', 'value'),
     Input('number_sim','value'),
     Input('number_paths','value'),
     Input('Spot','value'),
     Input('Underlying_dropdown','value'),
     Input('Rates_dropdown','value')
     ]
)



def update_output(n_clicks,number_call,Strike_call,Buy_Sell_call,number_put,Strike_put,Buy_Sell_put,Maturity,tab,number_sim,number_paths,Spot,Underlying_dropdown,Rates_dropdown):
    


#Definition of all default values for the several inputs to avoid errors if the user remove entirely the value of an input
    
    if number_call==None:
        number_call=0
    if Strike_call==None:
        Strike_call=0
    if Buy_Sell_call==None:
        Buy_Sell_call=0
        
    if number_put==None:
        number_put=0
    if Strike_put==None:
        Strike_put=0
    if Buy_Sell_put==None:
        Buy_Sell_put=0 
  
    if Maturity==None:
        Maturity=1  
        
    if number_sim==None:
        number_sim=1
        
    if number_paths==None:
        number_paths=1  
        
    if Spot==None:
        Spot=0  
        
    if number_sim==None:
        number_sim=0    

 
    if n_clicks is None:
        raise PreventUpdate
    
    else:

        
#########################################################################################################################################################
#Definition of parameters classes for pricing
                
        class Configuration:
            def __init__(self,number_sim,T_maturity):
                self.number_sim=number_sim
                self.T_maturity=T_maturity
        
        
        
        class Parameters:
            def __init__(self,k_r,theta_r,sigma_r,St,vt,rho, kappa,theta,lamb,sigma,K_call,K_put,Call=0.,Put=0.):
                self.k_r=k_r
                self.sigma_r=sigma_r
                self.theta_r=theta_r
                self.St=St
                self.vt=vt
                self.rho=rho
                self.kappa=kappa
                self.theta=theta
                self.lamb=lamb
                self.sigma=sigma
                self.K_call=K_call
                self.K_put=K_put
                self.Call=Call
                self.Put=Put
                
                
#########################################################################################################################################################
#Definition of the function of pricing
                
        class Heston_generate:
            def __init__(self,parameters,configuration):
                self.parameters=parameters
                self.configuration=configuration
                
            def function_Heston_Vasicek(self):
                    all_St_rt_vt=np.zeros((self.configuration.T_maturity*3,self.configuration.number_sim))
                    
                    #Initialization of the parameters
                    vt=self.parameters.vt
                    St=self.parameters.St
                    
                    deltat=1/number_paths
                    
                    #Brownian motion used for the pricing
                    
                    B_S=np.random.normal(0,1,(self.configuration.T_maturity,self.configuration.number_sim))
                    B=np.random.normal(0,1,(self.configuration.T_maturity,self.configuration.number_sim))
                    B_r=np.random.normal(0,1,(self.configuration.T_maturity,self.configuration.number_sim))
                    B_v=self.parameters.rho*B_S+np.sqrt(1-self.parameters.rho**2)*B
                    
                    
                    #Choice of the rate used for  the pricing
                    if Rates_dropdown=='Euribor 3M':
                        rt=-0.004*4
                        sigma_r=0.0125
                        theta_r=-0.03
                        k_r=0.20
                        
                    elif Rates_dropdown=="Libor 3M USD":
                        rt=0.019*4
                        sigma_r=0.014
                        theta_r=0.02
                        k_r=0.20
                        
                    if Underlying_dropdown=='SX5E':
                        rho=0.6
                        kappa=1.0
                        theta=0.1
                        lamb=0
                        sigma=0.1
                        vt=0.1
                        
                    if Underlying_dropdown=='SPX':
                        rho=0.6
                        kappa=1.0
                        theta=0.1
                        lamb=0
                        sigma=0.1
                        vt=0.15          
                        
                    if Underlying_dropdown=='NIKKEI':
                        rho=0.6
                        kappa=1.0
                        theta=0.1
                        lamb=0
                        sigma=0.1
                        vt=0.14   
                        
                    #Initialization of the parameters for the pricing
                    nb_days=1
                    all_St_rt_vt[0]=St
                    all_St_rt_vt[configuration.T_maturity]=rt
                    all_St_rt_vt[2*configuration.T_maturity]=vt

                    #Loop on the maturity
                    while nb_days<configuration.T_maturity:
                        
                        #We compute the rate simulations by using Vasicek model
                        rt=rt+parameters.k_r*(parameters.theta_r-rt)*deltat+deltat*parameters.sigma_r*B_r[nb_days]
                        
                        #We compute the volatility simulations by using Heston model
                        vt=vt + self.parameters.kappa*(self.parameters.theta-np.maximum(vt,0))*deltat + self.parameters.sigma*np.sqrt(np.maximum(vt,0))*np.sqrt(deltat)*B_S[nb_days]
                        
                        #We use the simulated volatility and rate to compute the level of the underlying
                        St=St*np.exp((rt-0.5*vt)*deltat + np.sqrt(vt)*np.sqrt(deltat)*B_S[nb_days])
                                    
                        all_St_rt_vt[nb_days]=St
                        all_St_rt_vt[self.configuration.T_maturity+nb_days]=rt
                        all_St_rt_vt[2*self.configuration.T_maturity+nb_days]=vt
                        nb_days=nb_days+1
                                        
                                        
                    return all_St_rt_vt
    

        #Class used for the MonteCarlo simulations
        class MonteCarlo:
            def __init__(self,parameters,configuration):
                self.configuration=configuration
                self.parameters=parameters
                
            def Call_MC(self):
                all_St_rt_vt=np.zeros((2*configuration.T_maturity,configuration.number_sim))
                all_C=np.zeros((configuration.number_sim))
                all_St_rt_vt=Heston_generate(parameters,configuration).function_Heston_Vasicek()
                    
                dt=configuration.T_maturity/number_paths
                    
                #Parallelism Part: We use the parallelism method (basd on Joblib) to price our option 
                all_C=Parallel(n_jobs=10,backend="threading")\
                (delayed(Parallelism)(all_St_rt_vt,nb_sim,dt) for nb_sim in range(configuration.number_sim))
                    
                return np.mean(all_C)
                
                
            #Function used under parallelism for computing the price of an option at maturity corresponding to simulation nb_sim 
        if Buy_Sell_call=='Sell':
            number_call=-number_call
        if Buy_Sell_put=='Sell':
            number_put=-number_put
                
        #Function used under parallelism for computing the price of an option at maturity corresponding to simulation nb_sim  
        def Parallelism(all_St_rt,nb_sim,dt):
            return parameters.Call*max(all_St_rt[configuration.T_maturity-1,nb_sim]-parameters.K_call,0)*np.exp(-dt*all_St_rt[2*configuration.T_maturity-1,nb_sim])+parameters.Put*max(parameters.K_put-all_St_rt[configuration.T_maturity-1,nb_sim],0)*np.exp(-dt*all_St_rt[2*configuration.T_maturity-1,nb_sim])
        
    #Initialization of all required parameters for option pricing 
    configuration=Configuration(number_sim,Maturity*number_paths)    
    parameters=Parameters(k_r,theta_r,sigma_r,Spot,vt,rho, kappa,theta,lamb,sigma,Strike_call,Strike_put,number_call,number_put)

    #Initialization of all required parameters for option pricing 
    x_option=np.zeros(Maturity*number_paths)
    y_option=Heston_generate(parameters,configuration).function_Heston_Vasicek()
    
    #Initialization of all required data for the following graphics 
    data_vol=[] #Data for Volatility graph
    data_rate=[] #Data for Rate graph
    data_St=[] #Data for Underlying graph
   
    #Computation of the Simulation required for the several graphics
    if number_sim>100:
        number_sim_graph=100
    else:
        number_sim_graph=number_sim
        
    for i in range(Maturity*number_paths):
        x_option[i]=i
    for i in range(number_sim_graph-1):
        data_St.append({'x':x_option,'y':y_option[:Maturity*number_paths,i+1]}.copy())
        data_vol.append({'x':x_option,'y':y_option[Maturity*number_paths*2:,i+1]}.copy())
        data_rate.append({'x':x_option,'y':y_option[Maturity*number_paths:,i+1]}.copy())
    
    #Computation of the Option Price
    Result=round(MonteCarlo(parameters,configuration).Call_MC(),2)
    
    if tab == 'tab-1-example':#Vol graphic
        return Result,html.Div([
                html.H3(Underlying_dropdown+ ' Volatility Simulations'),
                dcc.Graph(
                            id='graph_vol',
                            figure={
                                    'data':data_vol,
                                    'layout': {
            'xaxis':{'title':'Time in days'},
            'yaxis':{'title':'Volatility'},
             'showlegend':False
        }
                                    }
                            )
                    ])
    elif tab == 'Rate_Tab':#Rate graphic
            return Result,html.Div([
            html.H3(Rates_dropdown+ ' Rate Simulations'),
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                    'data': data_rate,
                    'layout': {
            'xaxis':{'title':'Time in days'},
            'yaxis':{'title':Rates_dropdown},
            'showlegend':False
        }
                    
                }
            )
        ])
            
    elif tab == 'Underlying_Tab':#Underlying graphic
            return Result,html.Div([
            html.H3(Underlying_dropdown+ ' Underlying Simulations'),
            dcc.Graph(
                figure={
                    'data': data_St,
                            'layout': {
            'xaxis':{'title':'Time in days'},
            'yaxis':{'title':Underlying_dropdown +' (%)'},
            'showlegend':False
        }
                    
                }
            )
        ])
    exit
    

if __name__ == '__main__':
    app.run_server(debug=True)
