from django.shortcuts import render

import pandas as pd
from plotly.io import to_html
import plotly.graph_objects as go



# patients = pd.read_csv('C://Users/sujee/OneDrive/Desktop/Project/Covid19/media/IndividualDetails.csv')
# patients = pd.read_csv('media/IndividualDetails.csv')

csv_url = 'https://xkkxrmuyuyjmcnbajwgg.supabase.co/storage/v1/object/sign/cvs_file/IndividualDetails.csv'

# csv_url = "https://xkkxrmuyuyjmcnbajwgg.supabase.co/storage/v1/object/sign/cvs_file/IndividualDetails.csv?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJjdnNfZmlsZS9JbmRpdmlkdWFsRGV0YWlscy5jc3YiLCJpYXQiOjE3MTc5MzQyNDUsImV4cCI6MjE0OTkzNDI0NX0.4P8kzh6wT8PdfMxxZLsA2EpBW-oZO2aFIvH4IKO0VnE&t=2024-06-09T11%3A57%3A25.639Z"

patients = pd.read_csv(csv_url)

# Create your views here.
def index(request):
    total = patients.shape[0]
    active = patients[patients['current_status'] == 'Hospitalized'].shape[0]
    recovered = patients[patients['current_status'] == 'Recovered'].shape[0]
    deaths = patients[patients['current_status'] == 'Deceased'].shape[0]

    # getting requests for graph to be change
    graph = request.POST.get('picker', 'All')

    # graphs
    all_graph = generate_graph(patients, None, "Blue", "Analysis of all cases", "Total Cases")
    active_graph = generate_graph(patients, "Hospitalized", "Orange", "Analysis of active cases", "Total Active Cases")
    recovered_graph = generate_graph(patients, "Recovered", "Green", "Analysis of recovered cases", "Total Recovered Cases")
    death_graph = generate_graph(patients, "Deceased", "Red", "Analysis of death cases", "Total Death Cases")


    # scatter for total cases
    scatter = scatter_plot()

    context = {
        'total': total,
        'active': active,
        'recovered': recovered,
        'deaths': deaths,
        'graph': graph,
        'all_graph': all_graph,
        'active_graph': active_graph,
        'recovered_graph': recovered_graph,
        'death_graph': death_graph,
        'scatter': scatter,
    }
    return render(request, 'index.html', context)


# to generate graph
def generate_graph(patients, status, color, title, yaxis):
    if status is not None:
        df = patients[patients['current_status'] == 'Deceased']['detected_state'].value_counts().reset_index()
        trace = go.Bar(
            x = df['detected_state'],
            y = df['count'],
            marker = {'color': color},
        )
        data = [trace]
        layout = go.Layout(
            title = title,
            xaxis = {'title': 'States'},
            yaxis = {'title': yaxis},
        )
        fig = go.Figure(data=data, layout=layout)
        return to_html(fig, full_html=False, include_plotlyjs='cdn')
    else:
        df = patients['detected_state'].value_counts().reset_index()
        trace1 = go.Bar(
            x = df['detected_state'],
            y = df['count'],
            marker = {'color': color},
        )
        data1 = [trace1]
        layout1 = go.Layout(
            title = title,
            xaxis = {'title': 'States'},
            yaxis = {'title': yaxis},
        )
        fig1 = go.Figure(data=data1, layout=layout1)
        return to_html(fig1, full_html=False, include_plotlyjs='cdn')
    

# to geenrate scatter plot for total cases
def scatter_plot():
    total = patients['detected_state'].value_counts().reset_index(name='total').sort_values(by='detected_state')
    trace = go.Scatter(
        x = total['detected_state'],
        y = total['total'],
        mode = 'markers+lines',
        marker = {'size': 18, 'color': 'red'}
    )
    data = [trace]
    layout = go.Layout(
        
        xaxis = {'title': 'States'},
        yaxis = {'title': 'Total Number'}
    )
    fig = go.Figure(data=data, layout=layout)
    return to_html(fig, full_html=False, include_plotlyjs='cdn')