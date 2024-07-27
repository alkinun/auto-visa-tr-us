# Gmail info
SENDER_EMAIL = "alkinunl@gmail.com"
APP_KEY_GMAIL = "cenw fcwi zcih ediz"

SEND_EMAIL = True
AUTO_RESCHEDULE = True

SHOW_GUI = False
TEST_MODE = True #doesnt press `confirm reschedule` btn

# Don't change the following unless you know what you are doing said the wise portuguese man
DETACH = True
NEW_SESSION_AFTER_FAILURES = 5
NEW_SESSION_DELAY = 60
TIMEOUT = 10
FAIL_RETRY_DELAY = 30
DATE_REQUEST_DELAY = 30
DATE_REQUEST_MAX_RETRY = 60
DATE_REQUEST_MAX_TIME = 30 * 60
LOGIN_URL = "https://ais.usvisa-info.com/en-tr/niv/users/sign_in"
AVAILABLE_DATE_REQUEST_SUFFIX = "/days/{consulate_id}.json?appointments[expedite]=false"
APPOINTMENT_PAGE_URL = "https://ais.usvisa-info.com/en-tr/niv/schedule/{id}/appointment"
PAYMENT_PAGE_URL = "https://ais.usvisa-info.com/en-tr/niv/schedule/{id}/payment"
REQUEST_HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
}
