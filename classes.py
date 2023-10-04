from enum import Enum
import json
from bs4 import BeautifulSoup

class ClassType(Enum):
    Laboratory = 1
    Interactive = 2
    Lecture = 3

class Time:
    def __init__(self, weekday, time_window, room):
        self.weekday = weekday
        self.time_window = time_window
        self.room = room

class Class:
    def __init__(self, name, class_type):
        self.name = name
        self.class_type = class_type

class Schedule:
    def __init__(self):
        self.time_table_ = {}  # A dictionary to store classes with their times
        self.classes_ = {}
    
    def add_class(self, class_name, class_type, weekday, time_window, room):
        if class_name not in self.classes_:
            class_obj = Class(class_name, class_type)
            self.classes_[class_name] = class_obj
        time_obj = Time(weekday, time_window, room)
        
        if class_name in self.time_table_:
            self.time_table_[class_name].append(time_obj)
        else:
            self.time_table_[class_name] = [time_obj]

    def get_class_schedule(self, class_name):
        if class_name in self.time_table_:
            return self.time_table_[class_name]
        else:
            return []
    
    def export_json_timetable(self):
        timetable_json = {
            "version": 2,
            "appName": "NicePlan",
            "lessons": []
        }

        for class_name, times in self.time_table_.items():
            class_obj = self.classes_[class_name]
            for time_obj in times:
                lesson_entry = {
                    "hexColor": "#ff3a2fff",  # You can customize the color
                    "room": time_obj.room,
                    "endTime": f"01-01-1970 {time_obj.time_window[1]}",
                    "day": time_obj.weekday,
                    "subject": class_obj.name,
                    "startTime": f"01-01-1970 {time_obj.time_window[0]}"
                }
                timetable_json["lessons"].append(lesson_entry)

        return json.dumps(timetable_json, indent=2)
    
html_table = """
<table class="table table-bordered table-striped" id="tb">
        <tr>
            <th style="width:50px; background-color: #428bca; color: white;">
                
            </th>
            <th style="background-color: #428bca; color: white;">
                Poniedziałek / Monday
            </th>
            <th style="background-color: #428bca; color: white;">
                Wtorek / Tuesday
            </th>
            <th style="background-color: #428bca; color: white;">
                Środa / Wednesday
            </th>
            <th style="background-color: #428bca; color: white;">
                Czwartek / Thursday
            </th>
            <th style="background-color: #428bca; color: white;">
                Piątek / Friday
            </th>
        </tr>

            <tr>
                <td>
                    07:00
                </td>

                    <td></td>

                    <td></td>


                    <td></td>

<td class='indiv' style='background-color:#FFE9FA'><b><a class='room_name' href='/Planner/ScheduleForRoom/NE160'>NE 160</a></b><br><b>[L]</b> <a class='subject_name' href='#'>Współczesne środowiska programowania</a><br>mgr inż. Kajetan Kruczkowski<br><b>od 07.12.2023</b></td>
                    <td></td>
            </tr>
            <tr>
                <td>
                    08:00
                </td>

<td class='indiv' style='background-color:#F8E6CE'><b><a class='room_name' href='/Planner/ScheduleForRoom/EA63'>EA 63</a></b><br><b>[L]</b> <a class='subject_name' href='#'>Podstawy robotyki - laboratorium</a><br>dr inż. Marek Tatara</td>
<td class='indiv' style='background-color:#F8E6CE'><b><a class='room_name' href='/Planner/ScheduleForRoom/NE239'>NE 239</a></b><br><b>[L]</b> <a class='subject_name' href='#'>Współczesne narzędzia obliczeniowe I</a><br>dr inż. Michał Czubenko<br><b>od 28.11.2023</b></td>

<td class='indiv' style='background-color:#D4EFFF'><b><a class='room_name' href='/Planner/ScheduleForRoom/EA31'>EA 31</a></b><br><b>[W]</b> <a class='subject_name' href='#'>Mikrosterowniki i mikrosystemy rozprosz</a><br>dr hab. Zbigniew Czaja</td>
<td class='indiv' style='background-color:#FFE9FA'><b><a class='room_name' href='/Planner/ScheduleForRoom/NE160'>NE 160</a></b><br><b>[L]</b> <a class='subject_name' href='#'>Współczesne środowiska programowania</a><br>mgr inż. Kajetan Kruczkowski<br><b>od 07.12.2023</b></td>
                    <td></td>
            </tr>
            <tr>
                <td>
                    09:00
                </td>

<td class='indiv' style='background-color:#F8E6CE'><b><a class='room_name' href='/Planner/ScheduleForRoom/EA63'>EA 63</a></b><br><b>[L]</b> <a class='subject_name' href='#'>Podstawy robotyki - laboratorium</a><br>dr inż. Marek Tatara</td>
<td class='indiv' style='background-color:#F8E6CE'><b><a class='room_name' href='/Planner/ScheduleForRoom/NE239'>NE 239</a></b><br><b>[L]</b> <a class='subject_name' href='#'>Współczesne narzędzia obliczeniowe I</a><br>dr inż. Michał Czubenko<br><b>od 28.11.2023</b></td>

<td class='indiv' style='background-color:#D4EFFF'><b><a class='room_name' href='/Planner/ScheduleForRoom/EA31'>EA 31</a></b><br><b>[W]</b> <a class='subject_name' href='#'>Mikrosterowniki i mikrosystemy rozprosz</a><br>dr hab. Zbigniew Czaja</td>
<td class='indiv' style='background-color:#F8E6CE'><b><a class='room_name' href='/Planner/ScheduleForRoom/EA31'>EA 31</a></b><br><b>[W]</b> <a class='subject_name' href='#'>Architektura systemów komputerowych</a><br>dr inż. Paweł Raczyński</td>
<td class='indiv' style='background-color:#FFE9E9'><b><a class='room_name' href='/Planner/ScheduleForRoom/SPNJOA2'>SPNJO A2</a></b><br><b>[C]</b> <a class='subject_name' href='#'>Język angielski IV</a><br>mgr Joanna Pawlik</td>            </tr>
            <tr>
                <td>
                    10:00
                </td>

<td class='indiv' style='background-color:#D4EFFF'><b><a class='room_name' href='/Planner/ScheduleForRoom/NEAUD.2'>NE AUD.2</a></b><br><b>[W]</b> <a class='subject_name' href='#'>Wstęp do sieci komputerowych</a><br>dr inż. Krzysztof Nowicki</td>
                    <td></td>


<td class='indiv' style='background-color:#EDEDED'><b><a class='room_name' href='/Planner/ScheduleForRoom/EA63'>EA 63</a></b><br><b>[L]</b> <a class='subject_name' href='#'>Podstawy robotyki - laboratorium</a><br>dr inż. Marek Tatara</td>
<td class='indiv' style='background-color:#F8E6CE'><b><a class='room_name' href='/Planner/ScheduleForRoom/EA31'>EA 31</a></b><br><b>[W]</b> <a class='subject_name' href='#'>Architektura systemów komputerowych</a><br>dr inż. Paweł Raczyński</td>
<td class='indiv' style='background-color:#FFE9E9'><b><a class='room_name' href='/Planner/ScheduleForRoom/SPNJOA2'>SPNJO A2</a></b><br><b>[C]</b> <a class='subject_name' href='#'>Język angielski IV</a><br>mgr Joanna Pawlik</td>            </tr>
            <tr>
                <td>
                    11:00
                </td>

<td class='indiv' style='background-color:#D4EFFF'><b><a class='room_name' href='/Planner/ScheduleForRoom/NEAUD.2'>NE AUD.2</a></b><br><b>[W]</b> <a class='subject_name' href='#'>Wstęp do sieci komputerowych</a><br>dr inż. Krzysztof Nowicki</td>
<td class='indiv' style='background-color:#D4EFFF'><b><a class='room_name' href='/Planner/ScheduleForRoom/AUD.NOV'>AUD.NOV</a></b><br><b>[P]</b> <a class='subject_name' href='#'>PROJEKT GRUPOWY I</a><br>dr inż. Sławomir Gajewski</td>

<td class='indiv' style='background-color:#EDEDED'><b><a class='room_name' href='/Planner/ScheduleForRoom/EA63'>EA 63</a></b><br><b>[L]</b> <a class='subject_name' href='#'>Podstawy robotyki - laboratorium</a><br>dr inż. Marek Tatara</td>
                        <td><b>NE AUD.2</b><br><b>[W]</b> <a class='subject_name' href='#'>Zasady przedsiębiorczości i zarządzania</a><br>dr hab. Marcin Gnyba</td>

<td class='indiv' style='background-color:#FCFF9C'><b><a class='room_name' href='/Planner/ScheduleForRoom/EA31'>EA 31</a></b><br><b>[W]</b> <a class='subject_name' href='#'>Współczesne środowiska programowania</a><br>dr hab. Tomasz Stefański<br><b>do 24.11.2023</b><br><b>EA 204</b><br><b>[L]</b> <a class='subject_name' href='#'>Wstęp do sieci komputerowych</a><br>dr inż. Krzysztof Nowicki<br><b>od 01.12.2023</b></td>            </tr>
            <tr>
                <td>
                    12:00
                </td>

<td class='indiv' style='background-color:#EDEDED'><b><a class='room_name' href='/Planner/ScheduleForRoom/EA32'>EA 32</a></b><br><b>[W]</b> <a class='subject_name' href='#'>Bazy danych</a><br>dr inż. Adam Bujnowski</td>
<td class='indiv' style='background-color:#D4EFFF'><b><a class='room_name' href='/Planner/ScheduleForRoom/AUD.NOV'>AUD.NOV</a></b><br><b>[P]</b> <a class='subject_name' href='#'>PROJEKT GRUPOWY I</a><br>dr inż. Sławomir Gajewski</td>

<td class='indiv' style='background-color:#FFE9E9'><b><a class='room_name' href='/Planner/ScheduleForRoom/EA532'>EA 532</a></b><br><b>[L]</b> <a class='subject_name' href='#'>Sterowanie analogowe - laboratorium</a><br>dr inż. Tomasz Białaszewski</td>
<td class='indiv' style='background-color:#EDEDED'><b><a class='room_name' href='/Planner/ScheduleForRoom/NE238'>NE 238</a></b><br><b>[L]</b> <a class='subject_name' href='#'>Bazy danych</a><br>mgr inż. Magdalena Madej<br><b>co 2 tygodnie</b></td>
<td class='indiv' style='background-color:#FCFF9C'><b><a class='room_name' href='/Planner/ScheduleForRoom/EA31'>EA 31</a></b><br><b>[W]</b> <a class='subject_name' href='#'>Współczesne środowiska programowania</a><br>dr hab. Tomasz Stefański<br><b>do 24.11.2023</b><br><b>EA 204</b><br><b>[L]</b> <a class='subject_name' href='#'>Wstęp do sieci komputerowych</a><br>dr inż. Krzysztof Nowicki<br><b>od 01.12.2023</b></td>            </tr>
            <tr>
                <td>
                    13:00
                </td>

<td class='indiv' style='background-color:#EDEDED'><b><a class='room_name' href='/Planner/ScheduleForRoom/EA32'>EA 32</a></b><br><b>[W]</b> <a class='subject_name' href='#'>Bazy danych</a><br>dr inż. Adam Bujnowski</td>
                        <td><b>EA 32</b><br><b>[W]</b> <a class='subject_name' href='#'>Metody numeryczne</a><br>mgr inż. Sebastian Dziedziewicz</td>


<td class='indiv' style='background-color:#FFE9E9'><b><a class='room_name' href='/Planner/ScheduleForRoom/EA532'>EA 532</a></b><br><b>[L]</b> <a class='subject_name' href='#'>Sterowanie analogowe - laboratorium</a><br>dr inż. Tomasz Białaszewski</td>
<td class='indiv' style='background-color:#EDEDED'><b><a class='room_name' href='/Planner/ScheduleForRoom/NE238'>NE 238</a></b><br><b>[L]</b> <a class='subject_name' href='#'>Bazy danych</a><br>mgr inż. Magdalena Madej<br><b>co 2 tygodnie</b></td>
                    <td></td>
            </tr>
            <tr>
                <td>
                    14:00
                </td>

<td class='indiv' style='background-color:#FFE9E9'><b><a class='room_name' href='/Planner/ScheduleForRoom/EA07'>EA 07</a></b><br><b>[W]</b> <a class='subject_name' href='#'>Współczesne narzędzia obliczeniowe I</a><br>dr inż. Michał Czubenko<br><b>do 20.11.2023</b><br><b>EA 204</b><br><b>[L]</b> <a class='subject_name' href='#'>Wstęp do sieci komputerowych</a><br>dr inż. Krzysztof Nowicki<br><b>od 27.11.2023</b></td>
<td class='indiv' style='background-color:#EDEDED'><b><a class='room_name' href='/Planner/ScheduleForRoom/EA532'>EA 532</a></b><br><b>[L]</b> <a class='subject_name' href='#'>Sterowanie analogowe - laboratorium</a><br>dr inż. Tomasz Białaszewski<br><b>NE 159</b><br><b>[L]</b> <a class='subject_name' href='#'>Współczesne narzędzia obliczeniowe I</a><br>dr inż. Michał Czubenko<br><b>od 28.11.2023</b></td>

                    <td></td>

                    <td></td>

                    <td></td>
            </tr>
            <tr>
                <td>
                    15:00
                </td>

<td class='indiv' style='background-color:#FFE9E9'><b><a class='room_name' href='/Planner/ScheduleForRoom/EA07'>EA 07</a></b><br><b>[W]</b> <a class='subject_name' href='#'>Współczesne narzędzia obliczeniowe I</a><br>dr inż. Michał Czubenko<br><b>do 20.11.2023</b><br><b>EA 204</b><br><b>[L]</b> <a class='subject_name' href='#'>Wstęp do sieci komputerowych</a><br>dr inż. Krzysztof Nowicki<br><b>od 27.11.2023</b></td>
<td class='indiv' style='background-color:#EDEDED'><b><a class='room_name' href='/Planner/ScheduleForRoom/EA532'>EA 532</a></b><br><b>[L]</b> <a class='subject_name' href='#'>Sterowanie analogowe - laboratorium</a><br>dr inż. Tomasz Białaszewski<br><b>NE 159</b><br><b>[L]</b> <a class='subject_name' href='#'>Współczesne narzędzia obliczeniowe I</a><br>dr inż. Michał Czubenko<br><b>od 28.11.2023</b></td>

                    <td></td>

                    <td></td>

                    <td></td>
            </tr>
            <tr>
                <td>
                    16:00
                </td>

                    <td></td>

                        <td><b>NE 160</b><br><b>[L]</b> <a class='subject_name' href='#'>Sztuczna inteligencja w automatyce - la</a><br>mgr inż. Piotr Kopa-Ostrowski</td>


                    <td></td>

                    <td></td>

                    <td></td>
            </tr>
            <tr>
                <td>
                    17:00
                </td>

                    <td></td>

                        <td><b>NE 160</b><br><b>[L]</b> <a class='subject_name' href='#'>Sztuczna inteligencja w automatyce - la</a><br>mgr inż. Piotr Kopa-Ostrowski</td>


                    <td></td>

                    <td></td>

                    <td></td>
            </tr>
            <tr>
                <td>
                    18:00
                </td>

<td class='indiv' style='background-color:#FFE9FA'><b><a class='room_name' href='/Planner/ScheduleForRoom/NE160'>NE 160</a></b><br><b>[L]</b> <a class='subject_name' href='#'>Współczesne środowiska programowania</a><br>mgr inż. Kajetan Kruczkowski<br><b>od 27.11.2023</b></td>
<td class='indiv' style='background-color:#F8E6CE'><b><a class='room_name' href='/Planner/ScheduleForRoom/EA108'>EA 108</a></b><br><b>[L]</b> <a class='subject_name' href='#'>Przetworniki wielkości nieelektrycznych</a><br>dr inż. Paweł Kalinowski</td>

                    <td></td>

                    <td></td>

                    <td></td>
            </tr>
            <tr>
                <td>
                    19:00
                </td>

<td class='indiv' style='background-color:#FFE9FA'><b><a class='room_name' href='/Planner/ScheduleForRoom/NE160'>NE 160</a></b><br><b>[L]</b> <a class='subject_name' href='#'>Współczesne środowiska programowania</a><br>mgr inż. Kajetan Kruczkowski<br><b>od 27.11.2023</b></td>
<td class='indiv' style='background-color:#F8E6CE'><b><a class='room_name' href='/Planner/ScheduleForRoom/EA108'>EA 108</a></b><br><b>[L]</b> <a class='subject_name' href='#'>Przetworniki wielkości nieelektrycznych</a><br>dr inż. Paweł Kalinowski</td>

<td class='indiv' style='background-color:#FCFF9C'><b><a class='room_name' href='/Planner/ScheduleForRoom/EA07'>EA 07</a></b><br><b>[P]</b> <a class='subject_name' href='#'>PROJEKT GRUPOWY I</a><br>dr inż. Janusz Kozłowski</td>
                    <td></td>

                    <td></td>
            </tr>
            <tr>
                <td>
                    20:00
                </td>

                    <td></td>

<td class='indiv' style='background-color:#F8E6CE'><b><a class='room_name' href='/Planner/ScheduleForRoom/EA108'>EA 108</a></b><br><b>[L]</b> <a class='subject_name' href='#'>Przetworniki wielkości nieelektrycznych</a><br>dr inż. Paweł Kalinowski</td>

<td class='indiv' style='background-color:#FCFF9C'><b><a class='room_name' href='/Planner/ScheduleForRoom/EA07'>EA 07</a></b><br><b>[P]</b> <a class='subject_name' href='#'>PROJEKT GRUPOWY I</a><br>dr inż. Janusz Kozłowski</td>
                    <td></td>

                    <td></td>
            </tr>
            <tr>
                <td>
                    21:00
                </td>

                    <td></td>

                    <td></td>


                    <td></td>

                    <td></td>

                    <td></td>
            </tr>

    </table>

"""
# Parse the HTML table using BeautifulSoup
soup = BeautifulSoup(html_table, 'html.parser')
schedule = Schedule()

# Find all table rows except the header
table_rows = soup.find_all('tr')[1:]

# Define a mapping for class types
class_type_mapping = {
    "Podstawy robotyki - laboratorium": ClassType.Laboratory,
    "Współczesne narzędzia obliczeniowe I": ClassType.Interactive,
    "Współczesne środowiska programowania": ClassType.Lecture,
    # Add more class types as needed
}

# Iterate through table rows and extract class information
for row in table_rows:
    columns = row.find_all('td')
    if len(columns) > 1:
        time_str = columns[0].text.strip()
        class_info = columns[1:]
        weekday = 0
        for col in class_info:
            class_details = col.find_all('a', class_='room_name')
            if class_details:
                room_name = class_details[0].text
                class_name = class_details[1].text
                class_type = class_type_mapping.get(class_name, None)
                if class_type:
                    schedule.add_class(class_name, class_type, weekday, (time_str, ''), room_name)
            weekday += 1

# Export the schedule to JSON format
json_schedule = schedule.export_json_timetable()
print(json_schedule)