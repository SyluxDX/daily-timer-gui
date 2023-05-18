# daily-timer
A graphical Timer for Daily Standup meetings

For a terminal based version check the sister project [Daily Timer](https://github.com/SyluxDX/daily-timer)


# Configurations
| Name              | Type        | Description                                                     |
|-------------------|-------------|-----------------------------------------------------------------|
| theme             | str         | UI theme selection, dark or light                               |
| time              | int         | Limit of seconds after which enter in overtime                  |
| warning           | int         | Number of seconds when an warning wil be displayed              |
| participants      | list of str | List of team members                                            |
| randomOrder       | bool        | Flag to randomize the participants list before each startup     |
| stopwatch         | bool        | Function mode flag. True: stopwatch, False: countdown           |
| stats.display     | bool        | Flag to display or hide statistics on member list               |
| stats.lastDailies | int         | Number of last dailies to include in the statistic calculations |


## Todo
- Add scroll logic, src/ui.py
