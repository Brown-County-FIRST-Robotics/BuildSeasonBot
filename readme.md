# install
git clone  git@github.com:Brown-County-FIRST-Robotics/BuildSeasonBot.git
cd BuildSeasonBot/
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt

# run
python bot.py 


# todo
- [ ] make competition names and dates configurable in settings
- [ ] make timezone configurable 
- [ ] use the timezone for establishing "today" and deciding when the periodic function should run instead of using bot-linux-server local date
- [ ] make so bot can run on more than one server easily
- [ ] add configure commands that can allow per-server(guild) configuration to be done by a server(guild) admin instead of modifying the settings.json
- [ ] make easily run as a daemon.  systemd?

