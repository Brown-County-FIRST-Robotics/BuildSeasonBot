# Install
```bash
git clone  git@github.com:Brown-County-FIRST-Robotics/BuildSeasonBot.git
cd BuildSeasonBot/
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```
# Run
```bash
python bot.py 
```

# Todo
- [ ] clean up and comment the code as if it wasn't written on the command line in a text editor now that others can see it
- [ ] make competition names and dates configurable in settings
- [ ] make timezone configurable 
- [ ] use the timezone for establishing "today" and deciding when the periodic function should run instead of using bot-linux-server local date
- [ ] make so bot can run on more than one server(guild) easily
- [ ] add configure commands that can allow per-server(guild) configuration to be done by a server(guild) admin instead of modifying the settings.json
- [ ] make easily run as a daemon.  systemd?
- [ ] once competition names and dates are configurable via command, allow scraping of bluealliance for auto populating

