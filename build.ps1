# create executable
Write-Host "Creating executable"
pyinstaller --log-level WARN --noconsole .\daily_timer_gui.py

# create one file executable
Write-Host "Creating on file executable"
pyinstaller --log-level WARN --clean --onefile --noconsole .\daily_timer_gui.py

# copy example config
Write-Host "Copying config"
Copy-Item .\team.json .\dist\daily_timer_gui\
Copy-Item .\team.json .\dist\

# create archive
Set-Location .\dist\
Write-Host "Creating archives"
Compress-Archive -path .\daily_timer_gui\ -destinationPath daily-timer-gui.zip
Compress-Archive -path .\daily_timer_gui\ -destinationPath daily-timer-gui_single-file.zip

# clean up
Write-Host "Clean up"
Remove-Item -Recurse -Force .\daily_timer_gui\
Remove-Item  .\daily_timer_gui.exe
Remove-Item  .\team.json

Set-Location ..
