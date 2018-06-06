import datetime


def getmealType():
    now = datetime.datetime.now()
    today7am = now.replace(hour=7, minute=30, second=0, microsecond=0)
    today10am = now.replace(hour=10, minute=0, second=0, microsecond=0)
    today12pm = now.replace(hour=12, minute=0, second=0, microsecond=0)
    today2pm = now.replace(hour=14, minute=30, second=0, microsecond=0)
    today7pm = now.replace(hour=19, minute=00, second=0, microsecond=0)
    today9pm = now.replace(hour=21, minute=30, second=0, microsecond=0)

    if now>=today7am and now<=today10am:
        meal_type = 'breakfast'
        isMeal = True

    elif now>=today12pm and now<=today2pm:
        meal_type = 'lunch'
        isMeal = True

    elif now>=today7pm and now<=today9pm:
        meal_type = 'dinner'
        isMeal = True

    else:
        isMeal = True
        meal_type = 'lunch'

    return isMeal, meal_type

isMeal, meal_type = getmealType()

print isMeal
print meal_type
