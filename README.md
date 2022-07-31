# Calendar Notifications
Get intrusive calendar notifications on your Mac for Zoom meetings with auto-join button. 

**Currently, only supports:**
- Platform: Apple macos
- Calendar: Any iCalendar calendar like Google Calendar.
- Joinable meeting notifications: Zoom.

**Note:** The implementation is highly extendable for other meeting tools. You'd just have to set up an `AbstractEventStartHandler` for your meeting tool. If you do add another meeting tool, please add a PR :).

## Features
- ✨ Notifications for meetings & recurring meetings.
- ⏱ Notifications for ToDos.
- 🖱️ Click on the notification to directly join the Zoom meeting.

## Requirements
This application was built on two libraries:
- [iCal-library](https://github.com/Jorricks/iCal-library)
- [macos-notifications](https://github.com/Jorricks/macos-notifications)

Please check them out and give them a 🌟. They were made with this project in mind 💡.

## Instructions
To use Calendar Notifications, you will need to:
1. Set up a new venv and install this tool in a new venv
    
       python3 -m venv venv/
       source venv/bin/activate
       pip3 install calendar-notifications

2. Get the iCalendar URL of your calendar. Instructions can be found in the [iCal-library remote iCalendar documentation section](https://jorricks.github.io/iCal-library/remote-icalendars/).
3. Enable python notifications. Instructions can be found in the [macos-notification FAQ](https://jorricks.github.io/macos-notifications/faq/).
4. Start it with `start_calendar_notifications`.

## DISCLAIMER
This project was developed after missing several meetings. I was looking for something more intrusive and ended up with this project. I went all-in on making sure it caught 100% of my Zoom meetings and that clicking the notification would immediately join the meeting for me. Although I did some effort productionising this, do not consider this as the holy grail. You might need to tweak it a little. Please file any [issues](https://github.com/Jorricks/calendar-notifications/issues) you encounter or submit a [pull-request](https://github.com/Jorricks/calendar-notifications/pulls) to fix it.
