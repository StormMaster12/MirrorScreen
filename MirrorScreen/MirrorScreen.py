# -*- coding: utf-8 -*-

import pyowm
import tkinter
import time
import calendar
import datetime
import math
import os
import httplib2

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

class WeatherModule():

    def __init__(self):
         #Initialises all of the Variables to use in this class
        self.img_clear = tkinter.PhotoImage(file="./mirrorscreen_images/clear.png")
        self.img_cloudy = tkinter.PhotoImage(file="./mirrorscreen_images/cloudy.png")
        self.img_mainly_cloudy = tkinter.PhotoImage(file="./mirrorscreen_images/mainly_cloudy.png")
        self.img_partialy_cloudy = tkinter.PhotoImage(file="./mirrorscreen_images/partialy_cloudy.png")
        self.list_weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    def Weather_Token(self,clouds,label):
        if (clouds <= 25):
            label.config(image=self.img_clear)   
        elif (clouds <=50 and clouds >25):
            label.config(image=self.img_partialy_cloudy)
        elif (clouds <=75 and clouds >50):
            label.config(image=self.img_mainly_cloudy)
        elif (clouds <=100 and clouds >75):
            label.config(image=self.img_cloudy)
        return

    def Rain_Ammount(self,rain,label):
        if (str(rain) == "None"):
            label.config(text=("  " + "0")+" mm",font=("Helvetica",8))
        else:
           label.config(text=("  " + str(rain)+" mm"),font=("Helvetica",8))

    def logic(self):

        owm_Main = pyowm.OWM("7cc5d2b85e2dd93f81b4810ad4927fc5")
        fc = owm_Main.daily_forecast('London, uk')
        f = fc.get_forecast()
        forecast_list= f.get_weathers()       
        #For Loop Goes through forecast, Starting at Positon 1.

        
        for index,item in enumerate(forecast_list[1:]):
            
            #Generates all the labels for the top part of the box. All Functions to reduce the size of the for loop
            date = item.get_reference_time('date')
            str_day_name =self.list_weekdays[date.weekday()]
            self.array_label_day_name[index].config(text=(str_day_name))
            self.array_label_cloud_forecast[index].config(text=(str(item.get_clouds()) +"%"))

            self.Weather_Token(item.get_clouds(),self.array_label_cloud_token[index])
            self.Rain_Ammount(item.get_rain().get("all"),self.array_label_rain_amount[index])
                    
        #Generates the Section of the Window for the Current Day.
        #Generates all the variables
        
        current_Temp = forecast_list[0].get_temperature("celsius")
        current_Cloud = forecast_list[0].get_clouds()
        current_Rain = forecast_list[0].get_rain().get("all")
        current_Day_Name = self.list_weekdays[forecast_list[0].get_reference_time('date').weekday()]

        #Draws all the information to the window
        self.label_current_Day_Name.config(text=(current_Day_Name))
        self.label_current_Cloud.config(text=(current_Cloud))
        self.label_current_Temp.config(text=(str(current_Temp['max'])+" °C"))
        self.Weather_Token(current_Cloud,self.label_current_Cloud_token)
        self.Rain_Ammount(current_Rain,self.label_current_rain_amount)

        self.frame_weather_container.after(3600000,self.logic)

    def Main(self,window):

        self.frame_weather_container = tkinter.Frame(window)

        self.frame_weather_container.pack(anchor=tkinter.NE,side=tkinter.RIGHT,padx=8)
        frame_weekday_container = tkinter.Frame(self.frame_weather_container)
        self.array_label_day_name = []
        self.array_label_cloud_forecast =[]
        self.array_label_rain_amount = []
        self.array_label_cloud_token =[]

        for i in range(0,6):

            frame_next_day = tkinter.Frame(frame_weekday_container)
            self.array_label_day_name.append(tkinter.Label(frame_next_day))
            self.array_label_cloud_forecast.append(tkinter.Label(frame_next_day))
            self.array_label_cloud_token.append(tkinter.Label(frame_next_day))
            self.array_label_rain_amount.append(tkinter.Label(frame_next_day))

            self.array_label_day_name[i].pack()
            self.array_label_cloud_token[i].pack()
            self.array_label_cloud_forecast[i].pack()
            self.array_label_rain_amount[i].pack()
            
            frame_next_day.pack(side=tkinter.LEFT)
        
        frame_weekday_container.pack()
        frame_Current_Day = tkinter.Frame(self.frame_weather_container)
        label_blank = tkinter.Label(frame_Current_Day).pack()
        self.label_current_Day_Name = tkinter.Label(frame_Current_Day)#,text=(current_Day_Name)).pack()
        self.label_current_Temp = tkinter.Label(frame_Current_Day)#,text=(current_Temp.get("max"))).pack()
        self.label_current_Cloud = tkinter.Label(frame_Current_Day)#,text=(str(current_Cloud)+" %")).pack()
        self.label_current_Cloud_token = tkinter.Label(frame_Current_Day)
        self.label_current_rain_amount = tkinter.Label(frame_Current_Day)

        self.label_current_Day_Name.pack()
        self.label_current_Temp.pack()
        self.label_current_Cloud_token.pack()
        self.label_current_Cloud.pack()
        self.label_current_rain_amount.pack()
        frame_Current_Day.pack()
        self.logic()

class ClockModule():

    def __init__(self):
        self.time1 = ''

    def tick(self):
        global time1
        # get the current local time from the PC
        time2 = time.strftime('%H:%M:%S')
        # if time string has changed, update it
        if time2 != self.time1:
            self.time1 = time2
            self.clock.config(text=time2)
        # calls itself every 200 milliseconds
        # to update the time display as needed
        # could use >200 ms, but display gets jerky
        self.clock.after(200, self.tick)

    def draw_box(self,window):
        frame_Clock = tkinter.Frame(window,background="red",width=7,height=1)
        self.clock = tkinter.Label(frame_Clock, font=('Helvetica', 30, 'bold'),width=7,height=1)
        print("Huh")
        self.clock.pack()  
        frame_Clock.grid(row=0,column=0,sticky=tkinter.N)

class CalenadarModule():

    def __init__(self):
        self.SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
        self.CLIENT_SECRET_FILE = 'client_id.json'
        self.APPLICATION_NAME = 'MirrorScreen'
        self.list_weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

        try:
            import argparse
            self.flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            self.flags = None

    def logic(self):
        
        self.day_value = int(datetime.datetime.today().weekday()+1)
        self.now = datetime.datetime.now()
        self.day_date = int(self.now.strftime("%d"))
        print("THIS IS THE DATE I SWEAR :" + str(self.day_date))
        #Loads in the Calendar

        itm_Calendar = calendar.month(int(self.now.strftime("%Y")),int(self.now.strftime("%m")),w = 2,l = 1)

        if self.day_value !=1 and self.day_date < 7:
            print("You sure i Should be in here?")
            self.day_date += self.day_value      
        #This is the name of the day returned as a number
        day_name = ((self.day_value)*3)-2
        #This is the date of the month
        if self.day_value <6 and self.day_date>=7:
            print("OKAY WHAT THE HELL")
            day_number = math.ceil(((self.day_date)/7))+3
        elif self.day_date >=6 or self.day_date<7:
            print("THIS IS WHERE I WANT TO BE DAM IT")
            day_number = math.ceil(((self.day_date)/7))+2


    
        day_line_column = str(day_number) +"."+str(day_name)
        day_line_column_next = str(day_number) +"."+str(day_name-1)

        print(self.day_date)
        print(self.day_value)
        print(day_name)
        print(day_line_column)

        #Brings the calendar into main window and highlights the current day
        self.text_Calendar.config( font=('courier', 12, 'bold'),width = 21, height = 7,highlightbackground="black",state=tkinter.NORMAL)
        self.text_Calendar.insert(tkinter.INSERT, itm_Calendar)

        self.text_Calendar.tag_remove("Current_Day" ,day_line_column_next)
        self.text_Calendar.tag_remove("Current_Day" ,day_line_column)

        self.text_Calendar.tag_add("Current_Day" ,day_line_column_next)
        self.text_Calendar.tag_add("Current_Day" ,day_line_column)

        self.text_Calendar.tag_configure("Current_Day", background="blue")
        self.text_Calendar.config(state=tkinter.DISABLED)
        


        google_events = self.GoogleCalendarAddition()

        self.label_date.config(text=("Today :" + self.now.strftime('%d/%m/%y')))
        
        text = ""
        self.label_event.config(text=text)
        for i in range(0,4):
            
            date = (self.now + datetime.timedelta(days=i)).strftime('%Y-%m-%d')

            if i == 0:
                day = "Today"
            elif i == 1:
                day = "Tomorrow"
            else:
                futureday_value = self.day_value + (i-1)
                if futureday_value > 7 : 
                    futureday_value -= 7
                day =self.list_weekdays[futureday_value]

            print("Date :" + date + "- Day : " + day)

            total_itterated = self.AddGoogle(google_events ,date,day,text)
        del text 

        self.frame_Calendar.after(100000,self.logic)


            
        
    def GoogleGetCredentials(self):
        #"""Gets valid user credentials from storage.

        #If nothing has been stored, or if the stored credentials are invalid,
        #the OAuth2 flow is completed to obtain the new credentials.

        #Returns:
        #    Credentials, the obtained credential.
        #"""
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                        'client_id.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if self.flags:
                credentials = tools.run_flow(flow, store, self.flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def GoogleCalendarAddition(self):
        """Shows basic usage of the Google Calendar API.

        Creates a Google Calendar API service object and outputs a list of the next
        10 events on the user's calendar.
        """
        credentials = self.GoogleGetCredentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        eventsResult = service.events().list(
            calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        return events
    
    def AddGoogle(self,google_events, date,day,google_text):
        doingsomething = False
        i = 0
        if not google_events:
            print('No upcoming events found.')

        for event in google_events:
            start = event['start'].get('dateTime', event['start'].get('date'))
           
            print( start[0:10])
            if date == start[0:10]:
                event_info = start[11:] + "  " + event['summary'] + "\n"
                if event.get('description') != None:
                    event_info += event['description']

                google_text = self.label_event.cget("text") +'\n' + day + " : " + date + "\n" + event_info + '\n'
                self.label_event.config(text=google_text)
                doingsomething = True
        else:
            if not doingsomething:
                doingsomething = False
                google_text = self.label_event.cget('text')+ '\n' + "Looks like you have nothing on " + day + "\n"
                self.label_event.config(text=google_text)

    def Main(self,func_window):

        self.frame_Calendar = tkinter.Frame(func_window)
        self.text_Calendar = tkinter.Text(self.frame_Calendar)
        frame_blank = tkinter.Frame(self.frame_Calendar)
        frame_blank.grid(row=1,column=0,rowspan=6,columnspan=1,padx=10, pady=5,sticky = tkinter.W+tkinter.E+tkinter.N+tkinter.S)
        self.text_Calendar.grid(row=10,column=0,sticky=tkinter.S)
        self.frame_Calendar.grid(row=10,column=0,sticky=tkinter.W)
        frame_google_day = tkinter.Frame(self.frame_Calendar)
        self.label_date = tkinter.Label(frame_google_day)
        self.label_date.grid()
        self.label_event = tkinter.Label(frame_google_day)
        self.label_event.grid()
        frame_google_day.grid()

        self.logic()





def main():
    window.overrideredirect(True)
    window.tk_setPalette(background='black',highlightbackground="black")
    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()
    window.geometry(str(width) + "x" + str(height))
    module_Weather = WeatherModule()
    module_Weather.Main(window)

    frame_left = tkinter.Frame()

    module_Calendar = CalenadarModule()
    module_Calendar.Main(frame_left)

    module_Clock = ClockModule()
    module_Clock.draw_box(frame_left)
    module_Clock.tick()
    
    frame_left.pack(side=tkinter.LEFT,anchor=tkinter.N)

    #schedule = BlockingScheduler()
    #schedule.add_job(module_Weather.logic,'interval',minutes=1)
    #schedule.add_job(module_Calendar.logic,'interval',minutes=1)

    window.mainloop()


window = tkinter.Tk()
if __name__ == '__main__':
        main()
