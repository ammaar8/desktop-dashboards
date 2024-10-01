import os
import configparser
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ATimeLogger import ATimeLoggerClient

MARKER_SIZE = 10

def get_weekly_data(client, start_date, end_date, graph_name, activity=False):
    """
    Fetch and resample data by week from either group hours or activity hours.
    """
    if activity:
        df = client.get_activity_hours(start_date, end_date, graph_name)
    else:
        df = client.get_group_hours(start_date, end_date, graph_name)
    return df.resample('W').sum()

def add_bar_trace(fig, df_weekly, row, col, color):
    """
    Add a bar trace to the figure.
    """
    fig.add_trace(
        go.Bar(
            x=df_weekly.index,
            y=df_weekly['hours'],
            marker=dict(color=color)
        ),
        row=row,
        col=col
    )

def configure_figure_layout(fig):
    """
    Configure the layout for the entire figure.
    """
    fig.update_layout(
        paper_bgcolor='rgb(0,0,0)',
        plot_bgcolor='rgb(0,0,0)',
        font_color='rgb(175, 175, 175)',
        width=1920,
        height=1080,
        showlegend=False,
        xaxis_showgrid=False,
        yaxis_zeroline=False,
        yaxis_showgrid=False,
        xaxis2_showgrid=False,
        yaxis2_zeroline=False,
        yaxis2_showgrid=False,
        xaxis3_showgrid=False,
        yaxis3_zeroline=False,
        yaxis3_showgrid=False,
        xaxis4_showgrid=False,
        yaxis4_zeroline=False,
        yaxis4_showgrid=False,
        xaxis5_showgrid=False,
        yaxis5_zeroline=False,
        yaxis5_showgrid=False,
        xaxis6_showgrid=False,
        yaxis6_zeroline=False,
        yaxis6_showgrid=False,
    )

def main():
    # Set start and end dates
    start_date = datetime(day=1, month=1, year=2024)
    end_date = datetime(day=31, month=12, year=2024)

    # Load configuration
    project_dir, _ = os.path.split(os.path.abspath(__file__))
    config = configparser.ConfigParser()
    config.read(os.path.join(project_dir, 'settings.ini'))

    # Initialize client
    client = ATimeLoggerClient(config['LOGIN']['username'], config['LOGIN']['password'])

    # Create a 2x2 subplot figure with titles
    fig = make_subplots(
        rows=2,
        cols=3,
        subplot_titles=(
            config['GRAPHS']['fig1_1'],
            config['GRAPHS']['fig2_1'],
            config['GRAPHS']['fig3_1'],
            config['GRAPHS']['fig1_2'],
            config['GRAPHS']['fig2_2'],
            config['GRAPHS']['fig3_2'],
        )
    )

    df_weekly = get_weekly_data(client, start_date, end_date, config['GRAPHS']['fig1_1'])
    add_bar_trace(fig, df_weekly, row=1, col=1, color='#636efa')

    df_weekly = get_weekly_data(client, start_date, end_date, config['GRAPHS']['fig1_2'])
    add_bar_trace(fig, df_weekly, row=2, col=1, color='#ef553b')

    df_weekly = get_weekly_data(client, start_date, end_date, config['GRAPHS']['fig2_1'])
    add_bar_trace(fig, df_weekly, row=1, col=2, color='lightslategray')

    df_weekly = get_weekly_data(client, start_date, end_date, config['GRAPHS']['fig2_2'], activity=True)
    add_bar_trace(fig, df_weekly, row=2, col=2, color='mediumseagreen')

    df_weekly = get_weekly_data(client, start_date, end_date, config['GRAPHS']['fig3_1'])
    add_bar_trace(fig, df_weekly, row=1, col=3, color='burlywood')

    df_weekly = get_weekly_data(client, start_date, end_date, config['GRAPHS']['fig3_2'])
    add_bar_trace(fig, df_weekly, row=2, col=3, color='cornsilk')

    # Configure the figure layout
    configure_figure_layout(fig)

    # Save the image
    output_path = os.path.join(project_dir, 'wallpaper_images', '2024.png')
    print("Writing Images")
    fig.write_image(output_path)

if __name__ == '__main__':
    main()
