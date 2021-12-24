from datetime import datetime, date, timedelta, time
import pandas as pd
import requests
import json
from requests import status_codes
from requests.models import HTTPBasicAuth


class ATimeLoggerClient:

    def __init__(self, email, password) -> None:
        self.auth_url = 'https://app.atimelogger.com'
        self.api_url = 'https://app.atimelogger.com/api/v2'
        self.timezone = None

        self.email = email
        self.password = password
        self.authenticated = False
        self.group_guids = {} # Name -> Guid
        self.group_names = {} # Guid -> Name
        self.group_activities = {} # Group Guid -> Activity Guids for Group
        self.activity_guids = {} # Name -> Guid
        self.activity_names = {} # Guid -> Name
        self.access_points = {
            'types': '/types',
            'intervals': '/intervals',
        }
        self._authenticate()
        self._get_activities()


    def _authenticate(self):
        req = requests.get(
            self.api_url + '/types',
            auth=HTTPBasicAuth(self.email, self.password)
        )

        if req.status_code == 200:
            self.authenticated = True
            print("Authenticated Successfully")
        elif req.status_code == 401:
            self.authenticated = False
            print("Authentication Failed")
        else:
            print("Authentication Failed")
            self.authenticated = False


    def _get_activities(self):
        req = requests.get(
            self.api_url + '/types',
            auth=HTTPBasicAuth(self.email, self.password),
        )
        for t in req.json()['types']:
            if t['guid'] not in self.group_guids.keys() and t['group'] is True:
                self.group_names[t['guid']] = t['name']
                self.group_guids[t['name']] = t['guid']
                self.group_activities[t['guid']] = []

        for t in req.json()['types']:
            if t['guid'] not in self.activity_names.keys() and t['group'] is False:
                if t['parent'] is not None:
                    self.group_activities[t['parent']].append(t['guid'])
                self.activity_names[t['guid']] = t['name']
                self.activity_guids[t['name']] = t['guid']

        return {
            'group_guids': self.group_guids,
            'group_name': self.group_names,
            'group_activities': self.group_activities,
            'activity_guids': self.activity_guids,
            'activity_names': self.activity_names
        }


    def _cook_data(self, df):
        df = df.astype({
            "activity": "str",
            "from": "datetime64",
            "to": "datetime64",
            "comment": "str"
        })

        switchers: pd.DataFrame = df[df["from"].dt.date != df["to"].dt.date]
        df = df.drop(switchers.index).reset_index(drop=True)
        switchers = switchers.reset_index(drop=True)

        switchers_split: pd.DataFrame = pd.DataFrame(columns=switchers.columns)
        for i in range(len(switchers)):
            activity = switchers.iloc[i]["activity"]
            comment = switchers.iloc[i]["comment"]

            start_day = switchers.iloc[i]["from"]
            start_day_end = start_day.replace(hour=23, minute=59, second=59)

            end_day = switchers.iloc[i]["to"]
            end_day_start = end_day.replace(hour=0, minute=0, second=0)

            switchers_split = switchers_split.append(
                {
                    'activity': activity,
                    'from': start_day,
                    'to': start_day_end,
                    'comment': comment
                }, ignore_index=True)

            switchers_split = switchers_split.append(
                {
                    'activity': activity,
                    'from': end_day_start,
                    'to': end_day,
                    'comment': comment
                }, ignore_index=True)

        df = df.append(switchers_split, ignore_index=True)
        df = df.sort_values(['from'], ascending=False).reset_index(drop=True)

        df["duration"] = df['to'] - df['from']
        df['date'] = df['from'].dt.date
        df['hours'] = df['duration'].dt.total_seconds().divide(3600).round(2)
        return df


    def _get_intervals(self, start, end, activities=None):
        if start is None or end is None:
            return "Please pick both dates"
        if activities is None:
            activities = list(self.activity_names.keys())

        payload = {
            'from': int(start.timestamp()),
            'to': int(end.timestamp()),
            'limit': 10000,
        }

        if activities is not None:
            payload['types'] = ",".join(activities)

        req = requests.get(
            self.api_url + self.access_points['intervals'],
            auth=HTTPBasicAuth(self.email, self.password),
            params=payload
            )

        intervals = []
        for interval in req.json()['intervals']:
            from_time = datetime.fromtimestamp(interval['from'])
            to_time = datetime.fromtimestamp(interval['to'])
            act_name = self.activity_names[interval['type']['guid']]
            comment = interval['comment']
            intervals.append([from_time, to_time, act_name, comment, ])

        if intervals == []:
            return pd.DataFrame()

        if (intervals[0][0].date() < intervals[0][1].date()):
            intervals[0][1] = datetime.combine(
                intervals[0][0].date(),
                time(hour=23, minute=59, second=59)
            )

        if (intervals[-1][0].date() < intervals[-1][1].date()):
            intervals[-1][0] = datetime.combine(
                intervals[-1][1].date(),
                time(hour=0, minute=0, second=0),
            )
        df = pd.DataFrame(intervals, columns=["from", "to", "activity", "comment"])
        return self._cook_data(df)


    def get_group_intervals(self, start, end, group_name):
        if group_name in self.group_guids.keys():
            group_guid = self.group_guids[group_name]
        else:
            print(f"{group_name} not found in groups. Available groups are {self.group_guids.keys()}")
            return pd.DataFrame()
        
        group_activities = self.group_activities[group_guid]

        df = self._get_intervals(start, end, activities=group_activities)
        return df


    def get_group_hours(self, start, end, group_name):
        if group_name in self.group_guids.keys():
            group_guid = self.group_guids[group_name]
        else:
            print(f"{group_name} not found in groups. Available groups are {self.group_guids.keys()}")
            return pd.DataFrame()
        
        group_activities = self.group_activities[group_guid]

        df = self._get_intervals(start, end, activities=group_activities)
        df['date'] = pd.to_datetime(df['date'])
        df = df[['date', 'hours']]
        period = pd.date_range(
            start,
            end,
            freq='D'
        )
        df = df.groupby('date').sum().reset_index()
        df = df.set_index('date')
        df = df.reindex(period, fill_value=0)
        return df

    def get_activity_hours(self, start, end, activity_name):
        if activity_name in self.activity_guids.keys():
            activity_guid = self.activity_guids[activity_name]
        else:
            print(f"{activity_name} not found in activities. Available activities are {self.activity_guids.keys()}")
            return pd.DataFrame()

        df = self._get_intervals(start, end, activities=[activity_guid])
        df['date'] = pd.to_datetime(df['date'])
        df = df[['date', 'hours']]
        period = pd.date_range(
            start,
            end,
            freq='D'
        )
        df = df.groupby('date').sum().reset_index()
        df = df.set_index('date')
        df = df.reindex(period, fill_value=0)
        return df