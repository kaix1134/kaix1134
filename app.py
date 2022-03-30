import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import datamodel

# ***************************************
# getting data from datamodel.py
# ***************************************

order = datamodel.connect()

# ***************************************
# create figure 1 - sales by employee
# ***************************************

fig_employee = px.bar(order, 
    x='emp_name', y='total',
    color='type', text='total', title='Sales by Employee',
    hover_data=[],
    labels={'total':'Total sales', 'emp_name':'Employee', 'type':'Product Type'})
fig_employee.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig_employee.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_tickangle=45)

# ***************************************
# create figure 2 - sales by product
# ***************************************

fig_product = px.bar(order,
    x='productname', y='total',
    color='type', text='total', title='Sales by Product',
    hover_data=[],
    labels={'total':'Total sales', 'productname':'Product', 'type':'Product Type'})
fig_product.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig_product.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_tickangle=45)

# ***************************************
# Activate the app
# ***************************************

dash_app = dash.Dash(__name__)
app = dash_app.server

# ***************************************
# Layout
# ***************************************

dash_app.layout = html.Div(
    children=[
        html.Div(className='row',
                children=[
                    html.Div(className='four columns div-user-controls',
                            children=[
                                html.H2('Employee Sales dashboard'),
                            ]
                    ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                            children=[
                                dcc.Graph(id="sales_employee", figure=fig_employee)
                            ]
                    ),
                ]
            ),
        html.Div(className='row',
                children=[
                    html.Div(className='four columns div-user-controls',
                            children=[
                                html.H2('Product Sales dashboard'),
                            ]
                    ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                            children=[
                                dcc.Graph(id="sales_product", figure=fig_product)
                            ]
                    ),
                ]
            )
    ]
)

# ***************************************
# initiating the app
# ***************************************
if __name__ == '__main__':
    dash_app.run_server(debug=True)
