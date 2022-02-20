from datetime import datetime
from ATimeLogger import ATimeLoggerClient
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import configparser
import os



MARKER_SIZE = 10
if __name__ == '__main__':
    project_dir, _ = os.path.split(os.path.abspath(__file__))
    config = configparser.ConfigParser()
    config.read(os.path.join(project_dir, 'settings.ini'))
    client = ATimeLoggerClient(config['LOGIN']['username'],config['LOGIN']['password'])

    # Graph 1
    df = client.get_group_hours(
        datetime(day=1, month=1, year=2022),
        datetime(day=31, month=12, year=2022),
        config['GRAPHS']['fig1_1']
    )
    fig = make_subplots(rows=2, cols=1)
    fig.add_trace(
        go.Scatter( 
            x=df.index,
            y=df['hours'],
            fill='tozeroy',
            line_color='#636efa'
        ),
        row=1,
        col=1
    )
    fig.add_trace(
        go.Scatter(
            x=[datetime.today().date()],
            y=[df.loc[datetime.today().strftime('%Y-%m-%d')]['hours']],
            mode='markers',
            marker_size=MARKER_SIZE,
            marker_color='#636efa'
        ),
        row=1,
        col=1
    )

    # Graph 2
    df = client.get_group_hours(
        datetime(day=1, month=1, year=2022),
        datetime(day=31, month=12, year=2022),
        config['GRAPHS']['fig1_2']
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df['hours'],
            fill='tozeroy',
            line_color='#ef553b'
        ),
        row=2,
        col=1
    )
    fig.update_layout(
        paper_bgcolor='rgb(0,0,0)',
        plot_bgcolor='rgb(0,0,0)',
        yaxis_range=[0, 16],
        yaxis2_range=[0, 16],
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
    fig.add_trace(
        go.Scatter(
            x=[datetime.today().date()],
            y=[df.loc[datetime.today().strftime('%Y-%m-%d')]['hours']],
            mode='markers',
            marker_size=MARKER_SIZE,
            marker_color='#ef553b'
        ),
        row=2,
        col=1
    )
    fig.add_vline(
        x=datetime.today().date(),
        line_color='green',
        line_dash='dash'
    )


    fig2 = make_subplots(rows=2, cols=1)
    # Graph 3
    df = client.get_group_hours(
        datetime(day=1, month=1, year=2022),
        datetime(day=31, month=12, year=2022),
        config['GRAPHS']['fig2_1']
    )

    fig2.add_trace(
        go.Scatter( 
            x=df.index,
            y=df['hours'],
            fill='tozeroy',
            line_color='lightslategray'
        ),
        row=1,
        col=1
    )
    fig2.add_trace(
        go.Scatter(
            x=[datetime.today().date()],
            y=[df.loc[datetime.today().strftime('%Y-%m-%d')]['hours']],
            mode='markers',
            marker_size=MARKER_SIZE,
            marker_color='lightslategray'
        ),
        row=1,
        col=1
    )
    # Graph 4
    df = client.get_activity_hours(
        datetime(day=1, month=1, year=2022),
        datetime(day=31, month=12, year=2022),
        config['GRAPHS']['fig2_2']
    )

    fig2.add_trace(
        go.Scatter(
            x=df.index,
            y=df['hours'],
            fill='tozeroy',
            line_color='mediumseagreen'
        ),
        row=2,
        col=1
    )
    fig2.update_layout(
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
    fig2.add_trace(
        go.Scatter(
            x=[datetime.today().date()],
            y=[df.loc[datetime.today().strftime('%Y-%m-%d')]['hours']],
            mode='markers',
            marker_size=MARKER_SIZE,
            marker_color='mediumseagreen'
        ),
        row=2,
        col=1
    )
    fig2.add_vline(
        x=datetime.today().date(),
        line_color='green',
        line_dash='dash'
    )


    print("Writing Images")
    fig.write_image(os.path.join(project_dir, 'wallpaper_images', 'desktopdashboard_screen1.png'))
    fig2.write_image(os.path.join(project_dir, 'wallpaper_images', 'desktopdashboard_screen2.png'))
