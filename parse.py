from bs4 import BeautifulSoup
import re
from classes import *
import argparse 


def get_type(cell):
    whole_text = cell.get_text()
    types = re.findall(r"\[([LCW])\]", whole_text)
    if len(types) == 0:
        return ClassType.Undefined
    try:
        return ClassType(types[0])
    except ValueError as e:
        print(f"Error: wrong char for ClassType inside: {types[0]}")
        return ClassType.Undefined


def main():
    parser = argparse.ArgumentParser(
            prog="SIS Plan parser",
            description="Convert class schedule from the site https://sis.eti.pg.edu.pl\nto other formats"
            )
    parser.add_argument("filename")
    parser.add_argument("-n", "--niceplan", action='store_true', help="Should a niceplan file be generated?")
    parser.add_argument("-i", "--ical", action='store_true', help="Should an ical file be generated?")
    html_content = ""
    args = parser.parse_args()
    with open(args.filename, mode="r", encoding="utf-8") as html_file:
        html_content = html_file.read()

    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find(
        "table", {"class": "table table-bordered table-striped", "id": "tb"}
    )
    # iterate over all rows
    hour = 6
    schedule = Schedule()
    for row in table.find_all("tr"):
        day = -1
        for cell in row.find_all("td"):
            day += 1
            # get the subject name of the class
            subject = cell.find("a", {"class": "subject_name"})
            # abort if cell is empty
            if subject == None:
                continue
            subject = re.sub(r"\s*-\s*\w*", "", subject.get_text())
            room_text = cell.find("a", {"class": "room_name"})
            room = ""
            if room_text != None:
                room = room_text.get_text()
            type = get_type(cell)
            time = Time(day - 1, hour, room)
            subject = Subject(subject, type)
            schedule.add_class(subject, time)
        hour += 1
    if args.niceplan:
        with open("output_time_table.niceplan", "w", encoding="utf-8") as f:
            data = schedule.export_json_niceplan()
            json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
    
    if args.ical:
        with open("output_time_table.ics", "w", encoding="utf-8") as f:
            data_ical = schedule.export_icalendar()
            for cell in data_ical:
                f.write(cell + '\n')

if __name__ == "__main__":
    main()
