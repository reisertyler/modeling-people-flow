
""" COPYRIGHT 2024 Tyler A Reiser. """


from datetime import datetime


###############################################################################
#
#   Event Dictionary
#
###############################################################################

events = {
    "CU Black and Gold scrimmage": {
        "2019": datetime.strptime("April 27, 2019 12:00 PM", "%B %d, %Y %I:%M %p"),
        "2022": datetime.strptime("April 23, 2022 12:00 PM", "%B %d, %Y %I:%M %p"),
        "2023": datetime.strptime("April 22, 2023 12:00 PM", "%B %d, %Y %I:%M %p")
    },
    "CU vs Nebraska": {
        "2019": datetime.strptime("Sep 7, 2019 1:30 PM" , "%b %d, %Y %I:%M %p"),
        "2023": datetime.strptime("Sep 9, 2023 10:00 AM", "%b %d, %Y %I:%M %p")
    },
    "Family Weekend": {
        "2019": datetime.strptime("Oct 5, 2019 2:30 PM", "%b %d, %Y %I:%M %p"),
        "2022": datetime.strptime("Oct 15, 2022 12:00 PM", "%b %d, %Y %I:%M %p"),
        "2023": datetime.strptime("Oct 13, 2023 8:00 PM", "%b %d, %Y %I:%M %p")
    },
    "CU vs USC": {
        "2019": datetime.strptime("Oct 25, 2019 7:00 PM", "%b %d, %Y %I:%M %p"),
        "2023": datetime.strptime("Sep 30, 2023 12:00 PM", "%b %d, %Y %I:%M %p")
    },
    "CU vs Stanford": {
        "2019": datetime.strptime("Nov 9, 2019 1:00 PM", "%b %d, %Y %I:%M %p"),
        "2023": datetime.strptime("Oct 13, 2023 8:00 PM", "%b %d, %Y %I:%M %p")
    },
    "Fall Classes Begin": {
        "2019": datetime.strptime("Aug 26, 2019", "%b %d, %Y")
    },
    "Labor Day Holiday": {
        "2019": datetime.strptime("Sep 2, 2019", "%b %d, %Y"),
    },
    "Thanksgiving Holiday": {
        "2019": datetime.strptime("Nov 28, 2019", "%b %d, %Y"),
        }
    }