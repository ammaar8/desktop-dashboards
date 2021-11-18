from datetime import datetime
from ATimeLogger import ATimeLoggerClient
import plotly.graph_objects as go
from plotly.subplots import make_subplots

if __name__ == '__main__':
    client = ATimeLoggerClient("Username", "Password")

    df = client.get_group_hours(
        datetime(day=1, month=1, year=2021),
        datetime(day=31, month=12, year=2021),
        'Group'
    )

    fig = make_subplots(rows=2, cols=1)
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['hours'],
            fill='tozeroy',
        ),
        row=1,
        col=1
    )

    df = client.get_activity_hours(
        datetime(day=1, month=1, year=2021),
        datetime(day=31, month=12, year=2021),
        'Single Activity',
    )
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['hours'],
            fill='tozeroy',
        ),
        row=2,
        col=1
    )
    fig.update_layout(
        paper_bgcolor='rgb(0,0,0)',
        plot_bgcolor='rgb(0,0,0)',
        xaxis_showgrid=False,
        yaxis_zeroline=False,
        yaxis_showgrid=False,
        xaxis2_showgrid=False,
        yaxis2_zeroline=False,
        yaxis2_showgrid=False,
        font_color='rgb(175, 175, 175)',
        width=1400,
        height=700,
        showlegend=False
    )

    fig.add_vline(
        x=datetime.today(),
        line_color='green',
        line_dash='dash'
    )

    print("Writing Image")
    fig.write_image('images/test.png')
