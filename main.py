from lesson_types import lessonTypes
from get_module_information import getModuleInformation, getCurrentAcademicYear, getCurrentSemester
from dateutil import parser
from collections import deque

weekdays = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday'
}


def generateFreeSlots():
    urls = []
    print("Please input the nusmods timetable URL for sharing. Input 'x' to stop.")
    while True:
        url = input()
        if url == 'x':
            break
        urls.append(url)

    if not urls:
        return
    timingsList = []
    for url in urls:
        timingsList.append(getLessonTimingsForOneTimetable(url))
    printFreeSlots(findInverseOfTimings(mergeTimings(timingsList)))


def printFreeSlots(timingsList):
    arr = [0] * 5
    for weekday, slots in timingsList.items():
        intervalString = ''
        for i, slot in enumerate(slots):
            if i != len(slots) - 1:
                intervalString += slot.__str__() + ', '
            else:
                intervalString += slot.__str__()
        arr[weekday] = (f'{weekdays[weekday]}: {intervalString}')
    print('\n'.join(arr))


def findInverseOfTimings(timingsList):
    for i, weekday in timingsList.items():
        timingsList[i] = findInverseOfDay(weekday)
    return timingsList


def findInverseOfDay(day):
    intervals = deque()
    start, end = '0800', '2100'
    if not len(day):
        intervals.append(TimeSlot(start, end))
        return list(intervals)
    if len(day) == 1:
        intervals.append(TimeSlot(start, day[0].startTime))
        intervals.append(TimeSlot(day[-1].endTime, end))
        return list(intervals)
    else:
        for i in range(len(day) - 1):
            startTime = day[i].endTime
            endTime = day[i + 1].startTime
            intervals.append(TimeSlot(startTime, endTime))
        if len(intervals) >= 1:
            intervals.appendleft(TimeSlot(start, day[0].startTime))
            intervals.append(TimeSlot(day[-1].endTime, end))
    return list(filter(lambda slot: slot.startTime != slot.endTime, intervals))


def mergeTimings(timingsList):
    weekdays = {}
    for timings in timingsList:
        for weekday, slot in timings.items():
            if weekday not in weekdays:
                weekdays[weekday] = []
            weekdays[weekday] += slot
    for _, weekday in weekdays.items():
        weekday.sort(key=lambda slot: slot.startTime)
    for i in range(5):
        weekdays[i] = merge(weekdays[i])
    return weekdays


def merge(intervals):
    out = []
    for i in intervals:
        if out and i.startTime <= out[-1].endTime:
            out[-1].endTime = max(out[-1].endTime, i.endTime)
        else:
            out += i,
    return out


def getLessonTimingsForOneTimetable(url):
    return getTimeSlots(parseUrl(url))


def parseUrl(url):
    modules = {}
    modulesArray = url.split("share?", 1)[1].split("&")
    for module in modulesArray:
        s = module.split("=")
        moduleName = s[0]
        modules[moduleName] = {}
        lessons = s[1].split(",")
        for lesson in lessons:
            lessonTypeString, lessonNumber = lesson.split(":")
            modules[moduleName][lessonTypes[lessonTypeString]] = lessonNumber
    return modules


def getTimeSlots(modules):
    timeSlots = {}
    acadYear = getCurrentAcademicYear()
    sem = getCurrentSemester()
    for moduleCode in modules:
        moduleInfo = getModuleInformation(acadYear, moduleCode)
        for lessonType in modules[moduleCode]:
            lessonNumber = modules[moduleCode][lessonType]
            timetable = getSemesterDataForModule(sem, moduleInfo)
            lessons = [x for x in timetable if (
                x['classNo'] == lessonNumber and x['lessonType'] == lessonType)]
            for lesson in lessons:
                weekday = parser.parse(lesson['day']).weekday()
                if weekday not in timeSlots:
                    timeSlots[weekday] = []
                timeSlots[weekday].append(
                    TimeSlot(lesson['startTime'], lesson['endTime']))
    return timeSlots


def getSemesterDataForModule(sem, moduleInfo):
    for semester in moduleInfo['semesterData']:
        if semester['semester'] == sem:
            return semester['timetable']


class TimeSlot:
    def __init__(self, startTime, endTime):
        self.startTime = startTime
        self.endTime = endTime
        super().__init__()

    def __str__(self):
        return f'{self.startTime} - {self.endTime}'


generateFreeSlots()
