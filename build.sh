#!/bin/sh
# create single executable
pyinstaller --onefile daily_timer_gui.py

# copy example config
echo "Copying config"
cp team.json dist/

# create archive
cd dist
echo "Creating archive"
tar -czvf daily-timer-gui.tar daily_timer_gui team.json

# # clean up
echo "Clean up"
rm daily_timer_gui team.json
