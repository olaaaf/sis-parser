from enum import Enum
import json
import uuid


class ClassType(Enum):
    Undefined = "U"
    Laboratory = "L"
    Interactive = "C"
    Lecture = "W"


class Time:
    def __init__(self, weekday, start_time, room, duration=1):
        self.weekday = weekday
        self.start_time = start_time
        self.room = room
        self.duration = duration

    def to_string(self):
        return f"Weekday: {self.weekday}, Time Window: {self.start_time}, Room: {self.room}, Duration: {self.duration}"


class Subject:
    def __init__(self, name, class_type):
        self.name = name
        self.class_type = class_type

    def to_string(self):
        return f"Name: {self.name}, Class Type: {self.class_type}"

    def __hash__(self):
        # Custom hash method based on name and class_type
        return hash((self.name, self.class_type))

    def __eq__(self, other):
        # Custom equality method based on name and class_type
        if isinstance(other, Subject):
            return self.name == other.name and self.class_type == other.class_type
        return False


class Schedule:
    def __init__(self):
        self.subjects_ = {}

    def add_class(self, subject: Subject, time: Time):
        if subject in self.subjects_:
            self.subjects_[subject].append(time)
        else:
            self.subjects_[subject] = [time]

    def export_json_niceplan(self):
        timetable_json = {"version": 2, "appName": "NicePlan", "lessons": []}

        for subject, times in self.subjects_.items():
            color = "#4361eeff"
            if subject.class_type == ClassType.Laboratory:
                color = "#f72585ff"
            if subject.class_type == ClassType.Interactive:
                color = "#7209b7ff"
            if subject.class_type == ClassType.Lecture:
                color = "#3a0ca3ff"
            for time in times:
                lesson_entry = {
                    "subject": subject.name,
                    "startTime": f"01-01-1970 {time.start_time}:15:00",
                    "endTime": f"01-01-1970 {time.start_time + time.duration}:00:00",
                    "hexColor": color,  # You can customize the color
                    "room": time.room,
                    "day": f"{time.weekday}",
                }
                timetable_json["lessons"].append(lesson_entry)

        return timetable_json
    
    def export_icalendar(self):
        timetable_ical = [
        "BEGIN:VCALENDAR",
        "PRODID:SIS-PARSER",
        "VERSION:2.0",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "BEGIN:VTIMEZONE",
        "TZID:Europe/Warsaw",
        "X-LIC-LOCATION:Europe/Warsaw",
        "BEGIN:DAYLIGHT",
        "TZOFFSETFROM:+0100",
        "TZOFFSETTO:+0200",
        "TZNAME:CEST",
        "DTSTART:19700329T020000",
        "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU",
        "END:DAYLIGHT",
        "BEGIN:STANDARD",
        "TZOFFSETFROM:+0200",
        "TZOFFSETTO:+0100",
        "TZNAME:CET",
        "DTSTART:19701025T030000",
        "RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU",
        "END:STANDARD",
        "END:VTIMEZONE"]
        # For ICalendar COLOR HAVE TO BE A CSS COLOR NAME
        for subject, times in self.subjects_.items():
            color = "#4361eeff"
            if subject.class_type == ClassType.Laboratory:
                color = "#f72585ff"
            if subject.class_type == ClassType.Interactive:
                color = "#7209b7ff"
            if subject.class_type == ClassType.Lecture:
                color = "#3a0ca3ff"
            for time in times:
                lesson_entry = [
                    "BEGIN:VEVENT",
                    "DTSTAMP:19960704T120000Z",
                    f"SUMMARY:{subject.name}[{subject.class_type.value}]{time.room}",
                    f"UID: {uuid.uuid4()}",
                    "STATUS:CONFIRMED",
                    "TRANSP:OPAQUE",
                    "RRULE:FREQ=WEEKLY",
                    f"COLOR:{color}",
                    f"DTSTART;TZID=Europe/Warsaw:{str(20231002+time.weekday)}T{'' if time.start_time > 9 else '0'}{time.start_time}1500",
                    f"DTEND;TZID=Europe/Warsaw:{str(20231002+time.weekday)}T{'' if time.start_time >= 9 else '0'}{time.start_time + time.duration}0000",
                    "END:VEVENT"]
                timetable_ical += lesson_entry
                
        timetable_ical.append("END:VCALENDAR")
        
        return timetable_ical
    
    def merge_blocks(self):
        """
        Merges all same class blocks that are after each other and removes breaks between them.
        """
        for subject, times in self.subjects_.items():
            sorted_times = sorted(times, key=lambda x: (x.weekday, x.start_time))
            self.subjects_[subject] = sorted_times

        for subject, times in list(self.subjects_.items()):  # Using list to copy items for safe iteration
            merged_times = []
            current_time_block = None
            for time in times:
                if current_time_block is None:
                    # Initialize the first time block
                    current_time_block = Time(time.weekday, time.start_time, time.room, time.duration)
                else:
                    # Check if the current time block can be merged with the next one
                    if (time.weekday == current_time_block.weekday and
                        time.start_time == current_time_block.start_time + current_time_block.duration):
                        # Extend the current time block's duration
                        current_time_block.duration += time.duration
                    else:
                        # Save the current time block and start a new one
                        merged_times.append(current_time_block)
                        current_time_block = Time(time.weekday, time.start_time, time.room, time.duration)
            # Add the last time block
            if current_time_block is not None:
                merged_times.append(current_time_block)

            self.subjects_[subject] = merged_times