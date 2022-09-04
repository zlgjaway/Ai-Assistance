
import pyjokes
import wikipedia
from ai import AI
from todo import Todo, Item
from weather import Weather
from datetime import datetime
from calendar_skill import Calendar_skill
import dateparser
calendar = Calendar_skill()
calendar.load()
jaway = AI()
todo = Todo()

#calendar = Calendar_skill()
#calendar.load
# item = Item(title="get shopping")
# item = Item("potatoes")
# todo.new_item(item)
# todo.new_item(item2)
# If modifying these scopes, delete the file token.json.

def joke():
    funny = pyjokes.get_joke()
    print (funny)
    jaway.say("here is your favorite joke," + funny)

def weather():
    myweather = Weather()
    forecast = myweather.forecast
    # print(forecast)
    jaway.say(forecast)

def add_todo()->bool:
    item = Item()
    jaway.say("Tell me what to add to the list")
    try:
        item.title = jaway.listen()
        todo.new_item(item)
        message = "Added " + item.title
        jaway.say(message)
        return True
    except:
        print("oops there was an error")

        return False
 
def wiki_1()->bool:
    try:
        question = command.replace('who', '')
        
        asnwer =  wikipedia.summary(question, 1)
        jaway.say(asnwer)
        print (asnwer)
        return True
    except:
        print("can you ask again?")
        jaway.listen()
        return False

def wiki_2()->bool:
    try:
        question1 = command.replace("what",'')
        asnwer1 =  wikipedia.summary(question1, 1)
        jaway.say(asnwer1)
        print (asnwer1)
        return True
    except:
        print("can you ask again?")
        jaway.listen()
        return False

def list_todos():
    if len(todo) > 0:
        jaway.say("Here are your to do's")
        for item in todo:
            jaway.say(item.title)
    else:
        jaway.say("The to do list is empty!")
def remove_todo()->bool:
    jaway.say("Tell me which item to remove")
    try:
        item_title = jaway.listen()
        todo.remove_item(title=item_title)
        message = "Removed " + item_title
        jaway.say(message)
        return True
    except:
        print("opps there was an error")
        return False


def add_event()->bool:
    jaway.say("What is the name of the event")
    try:
        event_name = jaway.listen()
        jaway.say("When is this event?")
        event_begin = jaway.listen()
        event_isodate = dateparser.parse(event_begin).strftime("%Y-%m-%d %H:%M:%S")
        jaway.say("What is the event description?")
        event_description = jaway.listen()
        message = "Ok, adding event" + event_name
        jaway.say(message)
        calendar.add_event(begin=event_isodate, name=event_name, description=event_description)
        calendar.save()
        return True
    except:
        print("opps there was an error")
        return False
def remove_event()->bool:
    jaway.say("What is the name of the event you want to remove?")
    try:
        event_name = jaway.listen()
        try:
            calendar.remove_event(event_name=event_name)
            jaway.say("Event removed successfully")
            calendar.save()
            return True
        except:
            jaway.say("Sorry I could not find the event",event_name)
            return False
    except:
        print("opps there was an error")
        return False

def list_events(period):
    this_period = calendar.list_events(period=period)
    if this_period is not None:
        message = "There "
        if len(this_period) > 1:
            message = message + 'are '
        else:
            message = message + 'is '
        message = message + str(len(this_period)) 
        if len(this_period) > 1:
            message = message + ' events'
        else:
            message = message + ' event'
        print(message)
        jaway.say(message)
        for event in this_period:
            # alf.say(event.begin.datetime)
            event_date = event.begin.datetime
            weekday = datetime.strftime(event_date, "%A")

            print(weekday, type(weekday))
            day = str(event.begin.datetime.day)
            month = datetime.strftime(event_date, "%B")
            year = datetime.strftime(event_date, "%Y")
            message = "On " + weekday + " " + day + " of " + month + " " + year
            print(message)
            jaway.say(message)
            name = event.name
            print("name is:",name)
            message = "there is an event called " + name
            jaway.say(message)
            description = event.description
            message = "the event description is " + description
            print("description is:",description)
            jaway.say(message)

command = ""          
wake = "hey AJ"
jaway.say("Hello")

while True :
    try:
        command = jaway.listen()
        if command.count(wake) > 0:
            jaway.say("how can i help you")
            command = jaway.listen()
            if "what" in command:
                wiki_2()
                command = ""
            if "who" in command:
                wiki_1()
                command = ""
            
            if 'joke' in command:
                joke()
                command = ""

            if 'add' in command:
                add_todo()
                command = ""
            if  "to do" in command :
                list_todos()
                command = ""
            if  "remove" in command:
                remove_todo()
            if  "weather" in command:
                weather()
            if command in ["good morning" , "good afternoon", "good evening"]:
                now = datetime.now()
                hr = now.hour
                if hr <= 0 <=12:
                    message = "Morning"
                if hr >=12 <= 17:
                    message = "Afternoon"
                if hr >=17 <=21:
                    message = "Evening"
                if hr > 21: 
                    message = "Night"
                message = "Good " + message + " Long"
                jaway.say(message)
                weather()
                list_todos()  
            if command in ['add event','add to calendar','new event','add a new event']:
                add_event()
            if command in ['delete event','remove event','cancel event']:
                remove_event()
            if command in ['list events',"what's on this month","what's coming up this month"]:
                list_events(period='this month')
            if command in ["what's on this week","what's coming up this week"]:
                list_events(period='this week')
            if command in ['event']:
                list_events(period='all')
                                                                                                  
    except:
        print("oops there was an error")
        command = ""    


