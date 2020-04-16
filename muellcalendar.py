from icalendar  import Calendar, Event
from datetime import datetime
from pytz import UTC

def muellrequest():
    muell = open('muell.ics', 'rb')
    muellcal = Calendar.from_ical(muell.read())
    ls_muell = []

    for component in muellcal.walk():
        if component.name == "VEVENT":
            if component.get('summary') == "Gelber Sack":
                ls_muell.append(component.decoded('dtstart').date())
    muell.close()
    return ls_muell

def istodaymuell(muell):
    today = datetime.now().date()
    for date in muell:
        if today < date:
            datestr = date.strftime('%d.%m')
            return "Ihr müsst den Gelben Sack erst am " +datestr+ " vor die Tür stellen!"
            break
    else:
        return "Nein, heute müsst ihr nicht den gelben Sack vor die Tür stellen!"
    return istodaymuell(muell)