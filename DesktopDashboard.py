from datetime import datetime
from ATimeLogger import ATimeLoggerClient
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import configparser
import os



MARKER_SIZE = 10
if __name__ == '__main__':
    start_date = datetime(day=1, month=1, year=2024)
    end_date = datetime(day=31, month=12, year=2024)

    project_dir, _ = os.path.split(os.path.abspath(__file__))
    config = configparser.ConfigParser()
    config.read(os.path.join(project_dir, 'settings.ini'))
    client = ATimeLoggerClient(config['LOGIN']['username'],config['LOGIN']['password'])

    # Graph 1
    df = client.get_group_hours(
        start_date,
        end_date,
        config['GRAPHS']['fig1_1']
    )
    df_weekly = df.resample('W').sum()

    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            config['GRAPHS']['fig1_1'],
            config['GRAPHS']['fig2_1'],
            config['GRAPHS']['fig1_2'],
            config['GRAPHS']['fig2_2']
        ))

    fig.add_trace(
        go.Bar( 
            x=df_weekly.index,
            y=df_weekly['hours'],
            marker=dict(
                color='#636efa',
            )
        ),
        row=1,
        col=1
    )

    # Graph 2
    df = client.get_group_hours(
        start_date,
        end_date,
        config['GRAPHS']['fig1_2']
    )
    df_weekly = df.resample('W').sum()

    fig.add_trace(
        go.Bar(
            x=df_weekly.index,
            y=df_weekly['hours'],
            marker=dict(
                color='#ef553b'
            )
        ),
        row=2,
        col=1
    )
    # fig.update_layout(
    #     paper_bgcolor='rgb(0,0,0)',
    #     plot_bgcolor='rgb(0,0,0)',
    #     yaxis_range=[0, 7],
    #     yaxis2_range=[0, 7],
    #     xaxis_showgrid=False,
    #     yaxis_zeroline=False,
    #     yaxis_showgrid=False,
    #     xaxis2_showgrid=False,
    #     yaxis2_zeroline=False,
    #     yaxis2_showgrid=False,
    #     font_color='rgb(175, 175, 175)',
    #     width=1400,
    #     height=700,
    #     showlegend=False
    # )


    # fig2 = make_subplots(rows=2, cols=1)
    # Graph 3
    df = client.get_group_hours(
        start_date,
        end_date,
        config['GRAPHS']['fig2_1']
    )
    df_weekly = df.resample('W').sum()

    fig.add_trace(
        go.Bar( 
            x=df_weekly.index,
            y=df_weekly['hours'],
            marker=dict(
                color='lightslategray',
            )
        ),
        row=1,
        col=2
    )
    # # Graph 4
    df = client.get_activity_hours(
        start_date,
        end_date,
        config['GRAPHS']['fig2_2']
    )
    df_weekly = df.resample('W').sum()

    fig.add_trace(
        go.Bar(
            x=df_weekly.index,
            y=df_weekly['hours'],
            marker=dict(
                color='mediumseagreen',
            )
        ),
        row=2,
        col=2
    )

    fig.update_layout(
        paper_bgcolor='rgb(0,0,0)',
        plot_bgcolor='rgb(0,0,0)',
        font_color='rgb(175, 175, 175)',
        width=1920,
        height=1080,
        showlegend=False,
        
        # Settings for the first subplot
        xaxis_showgrid=False,
        yaxis_zeroline=False,
        yaxis_showgrid=False,
        
        # Settings for the second subplot
        xaxis2_showgrid=False,
        yaxis2_zeroline=False,
        yaxis2_showgrid=False,
        
        # Settings for the third subplot
        xaxis3_showgrid=False,
        yaxis3_zeroline=False,
        yaxis3_showgrid=False,
        
        # Settings for the fourth subplot
        xaxis4_showgrid=False,
        yaxis4_zeroline=False,
        yaxis4_showgrid=False
    )


    print("Writing Images")
    fig.write_image(os.path.join(project_dir, 'wallpaper_images', 'desktopdashboard_screen1.png'))
    # fig2.write_image(os.path.join(project_dir, 'wallpaper_images', 'desktopdashboard_screen2.png'))
