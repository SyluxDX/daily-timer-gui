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

#### Example
```json
{
    "theme": "dark",
    "time": 20,
    "warning": 10,
    "participants":[
        "John",
        "Marcus",
        "Abigal"
    ],
    "randomOrder": true,
    "stopwatch": false,
    "stats":{
        "display": true,
        "lastDailies": 30
    }
}
```

# Build from Source
### Linux
- Create a virtual enviroment
- Install the requiments specified in the file `requirements_linux.txt`
- Run PyInstaller on main script:
```sh
$ pyinstaller --onefile daily_timer_gui.py
```

### Windows
- Create a virtual enviroment
- Install the requiments specified in the file `requirements_windows.txt`
- Run PyInstaller on main script:
```sh
$ pyinstaller --noconsole daily_timer.py
```
The script compilation can be done with a single output file with the following line, but it may the flaged as a false-positve for virus and mallware. This is due to the executable not being signed, which requires paying for a certificate.
```sh
$ pyinstaller --onefile --noconsole daily_timer_gui.py
```
