# ToDoListTelegramBot

It is a repo for Telegram TODOList Bot.  
It can help to organize your events (see commands below) and keep track of your deadlines.

# Commands

This bot can handle commands from Telegram chat. For now supported commands are:  

* List all supported commands:
```
/help
```  

* Create new event/deadline:
```
/add <event_name> <date> <time>
```
Syntax:  
```<event_name>``` - various name in any format  
```<date>``` - date in format dd.mm.yyyy or dd/mm/yyyy  
```<time>``` - [optional if ```<date>``` is set] time in format hh:mm  

* Remove existing event/deadline by ID (to see the ID's of events type /show):
```
/remove <event_id>
```

* Show all existing events and deadlines:
```
/show
```

* :) A little easter egg, if you want something new:
```
/joke
``` 
