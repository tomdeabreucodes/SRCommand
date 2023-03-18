# SRCommand
![](https://img.shields.io/github/license/artfulinfo/SRCommand)

A self-hosted PB fetcher for speedrunners on streaming platforms, ideal for integration with general purpose bots such as StreamElements.

## Contents
[1. Features](#1-Features)\
[2. Setup](#2-Setup)\
[3. Usage](#3-Usage)\
[4. Run Locally](#4-Run-Locally)

## 1. Features
* Configuration GUI to add your desired games and categories
* Commands to grab PBs on SRDC right from your twitch chat
    * Specify game + category to get a specific PB
    * Specify game only and get all category PBs
    * Optional SRDC username argument to look up other people's PBs (otherwise defaulting to your base user)
    * Operates on aliases, resulting in compact commands that make sense for your game/community
    * Automatically generated help and about command, tailored to your config

## 2. Setup
You can deploy SRCommand to your platform of choice, following your provider's respective Django deplyoyment guide.

SRCommand takes minimal system resources to run, so it is possible to operate within PythonAnywhere's free tier. It is unlikely your storage or CPU usage will exceed the limitations placed on this service, so this will serve as an example implementation in this guide.

### 2.i. Deploying to PythonAnywhere
PythonAnywhere is an online integrated development environment (IDE) and web hosting service - a popular choice for running prototypes or small scale applications for free.

They have an excellent guide for getting started with an existing Django application, and this will get you most of the way there. Please follow their steps, while referring to the modifications detailed below that will be required to get it up and running.

[Deploying an existing Django project on PythonAnywhere](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)

**Configuration Details**\
Often these can be used as 1:1 replacement, however certain steps may vary based on user-specific factors. In these cases it will be indicated by placeholders e.g. `<PythonAnywhere-username>`. The `Section` column maps to the guide linked above for convenience.

| Section                              | Step                        | Location                                               | Action                                                                                                                                 |
| ------------------------------------ | --------------------------- | ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| Uploading your code                  | Clone Git Repository        | Bash Console                                           | `git clone https://github.com/artfulinfo/SRCommand`                                                                                    |
| After creating/activating virtualenv | Install Dependencies        | Bash Console                                           | `cd SRCommand`<br>`pip3 install -r requirements.txt`                                                                                   |
| Editing WSGI file                    | Overwrite Default WSGI      | Web > Code > WSGI Configuration File                   | Replace with contents from `pythonanywhere_wsgi.py` from the repo. Update path to `path = '/home/<PythonAnywhere-username>/SRCommand'` |
| Database setup                       | Run Migrations              | Bash Console (~/SRCommand)                             | `python3 manage.py migrate`                                                                                                            |
| Additional configuration             | Add SECRET_KEY              | Bash Console (~/SRCommand)                             | `echo "export SECRET_KEY=<Secret Key>" >> .env`                                                                                        |
| Additional configuration             | Update STATIC_ROOT          | Files > `~/SRCommand/srdctwitchbot/server_settings.py` | `STATIC_ROOT = "/home/<PythonAnywhere-username>/SRCommand/static"`                                                                                     |
| Additional configuration             | Prepare static files        | Bash Console (~/SRCommand)                             | `python3 manage.py collectstatic`                                                                                                      |
| Additional configuration             | Update static file location | Web > Static files                                     | url: `/static/` <br>Directory: `/home/<Pythonanywhere-username>/SRCommand/static/`                                                     |
| Additional configuration             | Update allowed hosts        | Files > `~/SRCommand/srdctwitchbot/server_settings.py` | `ALLOWED_HOSTS = ["<PythonAnywhere-username>.eu.pythonanywhere"]` (remove `.eu` if not using the European server)                      |

**Create Superuser**\
The config GUI for setting up your SRDC information and adding your games/categories/aliases is secured by an `IsAdmin` permission check, to make sure only you (or other trusted users) can edit your config.

Open up a bash console and create a new superuser login and complete the prompts:
```
cd SRCommand
python3 manage.py createsuperuser
```

By this point, everything should be in place for you to be able to start using the app.

Navigate to `<your-domain>.com/admin/` and you should be able to login using the details created above.

**Check its working**\
Now navigate to `<your-domain>.com/config/` and if you see the Games page, you're in.

**Additional considerations**
* In the repo, a dev_settings file is also provided, and a commented line to point django to this file in `manage.py`. Please do not use anything other than the server_settings in a live environment as it will not be secure.
* Please also familiarise yourself with any warnings/guidance on the PythonAnywhere guide, as well as [Django's production checklist](https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/).
* PythonAnywhere requires you to login occasionally and click `Run until 3 months from today` in your `Web` tab as a measure to avoid inactive free-tier apps running indefinitely. Keep an eye out for an email which should remind you to login when it is close to expiring

**Troubleshooting**\
Click `Web` and scroll down to `Logs`. The `Error log` is the most helpful tool in finding the cause of the site not loading.

### 2.ii. Command Settings
**Configure SRDC User (Required)**\
Search your SRDC username and click `Add` to set it as the default search when no specific username is provided.

**Configure Games (Required)**\
Search games by their full name, or SRDC abbreviation and click `Add`. Note that the abbreviation will be added by default as a `Twitch command alias` but you can remove this, and/or add more. Regardless of which one someone uses in the command, it will still work.

**Configure Categories (Required)**\
Add all the categories from that game you wish to be included. If it is a `per-level` category, the first avaialble level will automatically selected, but can be altered in the dropdown. Add aliases here in the same way as games.

**Configure Filters (Optional)**\
For some categories, they will have associated `variables` which are used to differentiate run characteristics e.g. `Number of players` `Character`. Apply filters here if necessary, but the command will work without any applied. If you have multiple instances of the same category with different filters added, ensure you differentiate these with a good category alias, to make it clearer to users.

**Aliases**
* Aliases are case-insensitive
* The same category alias can be used for different games, but not for different categories within the same game

### 2.iii. Adding Command to Twitch Channel\
**Add custom command to stream elements**
Create a new command with the command name `pb`, user level to `Everyone` and response to:\
`${urlfetch <YOUR DOMAIN>/pb/${queryescape ${1:|' '}}}`

## 3. Usage
The core syntax of the command is as follows, with `[]` indicating optional arguments:
`!pb game_alias [category_alias] [srdc_username]`

At a minimum, a valid game alias must be provided. Here are the possible variations and example outcomes.

**_Only game_alias provided_**\
`!pb game_alias`\
Returns: PBs for all added categories within that game. Note: only works for the default user
Example:
```
!pb smb
0:47:38 #8 in Glitchless; 1:32:22 #12 in 100%; 0:36:32 #24 in Any%
```

**_Both game_alias and category_alias provided_**\
`!pb game_alias category_alias`\
Returns: Specific PB for the default user and extra details.
Example:
```
!pb smb any%
artfulinfo has a PB of 0:36:32 (#24) in smb any% https://www.speedrun.com/smb/run/zqv51oxm
```

**_Game, Category and srdc_username all provided_**\
`!pb game_alias category_alias srdc_username`\
Returns: Specific PB for the user provided. Note: if username not exact, an alternative match may be found. The actual user used, will be specified in the response.
Example:
```
!pb smb any% someuser
someuser has a PB of 0:34:22 (#24) in smb any% https://www.speedrun.com/smb/run/pew23pxm
```

**Helper Commands**\
There are 2 helper commands, giving the user access to information about the command from chat.
```
!pb help
Command: !pb game_alias [category_alias] [srdc_username] | Games: smb | Categories: 100%; any%; glitchless
```

```
!pb about
Command usage instructions + guide to get these commands on your channel: <your domain>.com/about
```
The link goes to a public page on your instance of the app, providing similar info to `!pb help`, with extra detail, as well as providing a link to this repo.

**Errors**\
In the event of an invalid category or game alias being provided, the response will simply be: `(Game|Category) code not found.` depending on which failed.

If the user, specified or default, does not have a pb in the game, the response will be `Someuser has no PBs in this game.`

If you experience any other persistent errors for searches you know to be valid, you can try to debug it in your PythonAnywhere (or your platform of choice's) built-in logs. Feel free to raise as an issue.

## 4. Run Locally
**Pre-requisites**\
_Python 3_\
If you do not have a modern version of Python installed, you can get one from https://www.python.org/downloads/. You can check if you have Python installed by running `python3 --version` from terminal. SRCommand was developed on `3.10.6` but any modern version should work.

**Clone the repo**\
If you want to try out the app locally for testing or development purposes, a dedicated settings file has been created to enable this with ease.

cd into your directory of choice and clone the repo to your machine.

`git clone https://github.com/artfulinfo/SRCommand.git`

Now, from your editor of choice, open `SRCommand/manage.py` and uncomment the line `os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'srdctwitchbot.dev_settings')`, then comment out the line directly below `os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'srdctwitchbot.server_settings')`. After editing the section should appear as below:
```
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'srdctwitchbot.dev_settings')
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE',
    #                       'srdctwitchbot.server_settings')
```

**Install dependencies**\
Set up a virtual environment to install your dependencies in, activate it, and run the install.

_mac/linux_
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
_windows_
```
python -m venv venv
venv/scripts/activate
pip install -r requirements.txt
```
**Setup the database**\
Run `python3 manage.py migrate` to perform migrations, you will see a SQLite file appear in the project root.

**Create superuser**\
_See 2.i._\
Between creating the user and testing if you can login, you'll need to run `python3 manage.py runserver`

**Success**\
If you're able to login and access the `/config/` in the local server, you are setup and should now be able to continue from section 2.ii onwards. with all of the core functionality.

**Note**\
As mentioned in section 2, please do not deploy with the `dev_settings` still applied as is is not secure. So if you decide to deploy your local version, switch back to `server_settings` in `manage.py`. Refer to the [Django's production checklist](https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/) for additional details/guidance.
