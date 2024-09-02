import plotly.graph_objects as go
from util.variables import *
import chart_studio
chart_studio.tools.set_credentials_file(username='EynardM', api_key='••••••••••')
chart_studio.tools.set_config_file(world_readable=False, sharing='private')

models = ['n_train', 'n_aug', 's_train', 's_aug', 'm_train', 'm_aug', 'l_train', 'l_aug']

accuracies = {
    'n_train': [0.78, 0.58, 0.88, 0.77],
    'n_aug': [0.76, 0.60, 0.91, 0.68],
    's_train': [0.77, 0.54, 0.89, 0.69],
    's_aug': [0.81, 0.57, 0.91, 0.65],
    'm_train': [0.78, 0.57, 0.88, 0.79],
    'm_aug': [0.76, 0.58, 0.90, 0.72],
    'l_train': [0.77, 0.58, 0.90, 0.67],
    'l_aug': [0.79, 0.68, 0.89, 0.73]
}

# Transformation of accuracies into a 2D array
accuracies_array = [accuracies[model] for model in models]

fig = go.Figure()

# Plotting the curves for each model
for i, model in enumerate(models):
    fig.add_trace(go.Scatter(x=list(INT_TO_LABELS.values()), y=accuracies[model], mode='lines+markers', name=model))

# Formatting the graph
fig.update_layout(
    xaxis=dict(
        title='Classes',
        tickangle=-45,
        tickmode='array',
        tickvals=list(INT_TO_LABELS.values()),
        ticktext=list(INT_TO_LABELS.values()),
        tickfont=dict(size=14)
    ),
    yaxis=dict(
        title='Accuracy',
        tickfont=dict(size=14)
    ),
    title='Models Performance in Terms of Accuracy',
    titlefont=dict(size=16)
)

# Display the graph
fig.show()
