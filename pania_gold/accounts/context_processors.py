from datetime import date

def daily_message(request):

    messages = [
        "امروز هم می‌تونه شروع یک معجزه باشه",
        "با امید قدم بردار، راه خودش پیدا میشه",
        "تو از چیزی که فکر می‌کنی قوی‌تری",
        "رویاهایت را باور کن، حتی اگر دورند",
        "هر لبخند، یک قدم به سوی حال خوبه",
        "تا امید هست، هیچ‌چیز تموم نشده",
        "حتی تاریک‌ترین شب‌ها، طلوعی در راه دارند",
    ]

    index = date.today().toordinal() % len(messages)
    return {'daily_message': messages[index]}
