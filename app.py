import sys
from math import floor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from flask import Flask, request
from pymessenger import Bot
import bs4
import os
import config

app = Flask(__name__)
PAGE_ACCESS_TOKEN = config.Config.PAGE_ACCESS_TOKEN
bot = Bot(PAGE_ACCESS_TOKEN)

VERIFICATION_TOKEN = config.Config.VERIFICATION_TOKEN

@app.route('/', methods=['GET'])
def verify():
    # webhook verification
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.challenge'):
        if not request.args.get('hub.verify_token') == VERIFICATION_TOKEN:
            return "Verification token mismatch", 403
        return request.args.get('hub.challenge'), 200
    return 'Chat Bot Website', 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    # log(data)

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                # IDs
                sender_id = messaging_event['sender']['id']
                # recipient_id = messaging_event['recipient']['id']
                log(f"Sender id: {sender_id}")

                if messaging_event.get('message'):
                    if messaging_event['message'].get('text'):
                        query = messaging_event['message']['text']
                        process_input(sender_id, query)

    return "ok", 200


def log(message):
    print(message)
    sys.stdout.flush()


def process_input(sender_id, query):
    weather_word = 'weather'
    movie_word = 'movie'

    if 'help' == query.lower():
        chatbot_help(sender_id)

    elif weather_word in query.lower():
        fetch_weather(sender_id, query)

    elif movie_word in query.lower():
        fetch_cinema(sender_id, query)

    else:
        greetings(sender_id)


def greetings(sender_id):
    reply = (f"Hello! I am a chat bot who can get the actual weather or the forecast for the next 10 days. "
             f"And I can get you the actual movies from the Cinema City Hungary\nWrite 'help' "
             f"to see how could you use those features")
    bot.send_text_message(sender_id, reply)


def chatbot_help(sender_id):
    reply = (f"You can get Szeged's weather or get the forecast for the next 10 days.\n"
             f"Also you can get the actual movies from the Cinema City theaters.\n \n \n"
             f"If you want to use the weather features, type: 'weather'.\n"
             f"If you want to choose the movie feature, "
             f"type: 'movie' to get more help")
    bot.send_text_message(sender_id, reply)


def fetch_cinema(sender_id, query):
    """
    Cinema menu selector
    """
    main_url = r"https://www.cinemacity.hu/#/buy-tickets-by-cinema?in-cinema=1126&at=2024-05-12&view-mode=list"

    get_movies_word = 'movie movies'

    # get all movies
    if get_movies_word in query.lower():
        get_actual_movies(sender_id, main_url)

    else:
        reply = f"To get the actual movies, type: 'movie movies'."
        bot.send_text_message(sender_id, reply)


def get_actual_movies(sender_id, main_url):
    """
    Function to get the actual movies on the Cinema City theaters
    """
    reply = {}

    # for heroku
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    #driver = webdriver.Chrome()
    driver.get(main_url)

    reply['type'] = "movie list"

    try:
        html = driver.page_source
        soup = bs4.BeautifulSoup(html, "html.parser")

        elements = []  # contains the movie's title and poster img

        body = soup.find("body")
        # wait to lead that whole html tag to get all of it's data
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'swiper-wrapper.pb-xs')))
        now_watchable_movie_container_div = body.find_all("div", class_="swiper-wrapper pb-xs")[0]
        movie_divs = now_watchable_movie_container_div.find_all("div", class_="swiper-slide")
        for movie_div in movie_divs:
            title = movie_div.select_one('.poster-title').text.strip()
            a_tag = movie_div.find("a")
            movie_details_url = a_tag.get("href")

            img_tags = a_tag.find('img', class_="img-responsive poster-image poster")

            image_link = img_tags.get("data-src") if img_tags.has_attr("data-src") else img_tags.get("src")

            element = {}
            element['title'] = title
            element['item_url'] = movie_details_url
            element['image_url'] = image_link
            element['buttons'] = [{
                'type': 'web_url',
                'title': 'Movie Details',
                'url': movie_details_url
            }]
            elements.append(element)

        # the elements list is too long for send in one
        # so send all data through many message
        max_elements_per_message = 10
        num_elements = len(elements)
        num_messages = (num_elements // max_elements_per_message +
                        (1 if num_elements % max_elements_per_message != 0 else 0))

        for i in range(num_messages):
            start_index = i * max_elements_per_message
            end_index = min((i + 1) * max_elements_per_message, num_elements)
            reply_data = {'template_type': 'generic', 'elements': elements[start_index:end_index]}
            send_generic_message(sender_id, reply_data)

    except Exception as e:
        reply = f"Error: {e}\nCannot get movies"
        bot.send_text_message(sender_id, reply)


def fetch_weather(sender_id, query):
    """
    Weather menu selector
    """
    today_weather_words = ['weather now', 'weather today']
    weather_forecast_for_this_week_word = "weather next days"

    # get today's weather
    if query.lower() in today_weather_words:
        get_actual_weather(sender_id)

    # get weather forecast for this week
    elif query.lower() == weather_forecast_for_this_week_word:
        get_weather_for_the_next_10_days(sender_id)

    else:
        reply = (f"To get the actual weather, type: 'weather now' or 'weather today'\n"
                 f"To get forecast for the next 10 days, type: 'weather next days'.")
        bot.send_text_message(sender_id, reply)


def get_actual_weather(sender_id):
    """
    Function to fetch today's actual weather status
    """
    url = r"https://weather.com/weather/today/l/46.24,20.11"
    response = requests.get(url, timeout=10)
    status_code = response.status_code
    if status_code == 200:
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        weather_div = soup.find('div', class_='HourlyWeatherCard--TableWrapper--1OobO')

        # tempreature
        temperature_div = weather_div.find_all('div')[0]
        temperature_span = temperature_div.find('span').text.strip()
        temperaureNum = int(temperature_span.split('°')[0])
        farenheit_to_celsius = floor((temperaureNum - 32) / 1.8)
        temperature = f"Temperature: {farenheit_to_celsius}°C"

        # condition
        weather_icon_div = weather_div.find('div', class_='Column--icon--2TNHl')
        weather_svg = weather_icon_div.find('svg')
        weather_title = weather_svg.find('title').text.strip()
        condition = f"Weather Condition: {weather_title}"

        # humidity
        precipitation_div = weather_div.find_all('div')[2]
        precipitation_span = precipitation_div.find('span').text.strip()
        precipitation_text = precipitation_span.split('Chance of Rain')[1].strip()
        precipitation = f"Chance of rain: {precipitation_text}"

        reply = f"Today's weather now:\n{temperature}\n{condition}\n{precipitation}"
        bot.send_text_message(sender_id, reply)
    else:
        reply = f"Failed to get response from weather website. Status code: {status_code}"
        bot.send_text_message(sender_id, reply)


def get_weather_for_the_next_10_days(sender_id):
    """
    Function to fetch the weather for this week
    """
    reply = {}
    reply['type'] = "forecast for the next 10 days"
    url = r"https://weather.com/weather/tenday/l/926c09c2f6c8e02c81f8906e3ebad7824f5c705f11b89a6ea2458d5443327cb3"
    response = requests.get(url, timeout=10)
    status_code = response.status_code
    if status_code == 200:
        elements = []

        soup = bs4.BeautifulSoup(response.content, "html.parser")
        container_div = soup.find('div', class_='DailyForecast--DisclosureList--nosQS')
        days_details = container_div.find_all('details', class_='DaypartDetails--DayPartDetail--2XOOV')
        for day in days_details:
            # get weekday
            h2_tag = day.find('h2', class_='DetailsSummary--daypartName--kbngc')
            weekday = h2_tag.text.strip()

            # get temperature
            temperature_div = day.find('div', class_='DetailsSummary--temperature--1kVVp')
            temperature_str = temperature_div.text.strip()  # ~ 57°/34°
            part_1 = temperature_str.split('/')[0].strip('°')
            if part_1 != '--':
                part_1 = f"{floor((int(part_1) - 32) / 1.8)}°"
            part_2 = temperature_str.split('/')[1].strip('°')
            if part_2 != '--':
                part_2 = f"{floor((int(part_2) - 32) / 1.8)}°"
            temperature = f"{part_1}/{part_2}"

            # get condition
            condition_div = day.find('div', class_='DetailsSummary--condition--2JmHb')
            svg_tag = condition_div.find('svg')
            title_tag = svg_tag.find('title')
            condition = title_tag.text.strip()

            # get rain chance
            rain_chance_div = day.find('div', class_='DetailsSummary--precip--1a98O')
            span_tag = rain_chance_div.find('span')
            rain_chance = span_tag.text.strip()

            element = {}
            element['title'] = weekday
            element['subtitle'] = f"{temperature}\nCondition: {condition}\nChance of rain: {rain_chance}"

            elements.append(element)

        # the elements list is too long for send in one
        # so send all data through many message
        max_elements_per_message = 10
        num_elements = len(elements)
        num_messages = (num_elements // max_elements_per_message +
                        (1 if num_elements % max_elements_per_message != 0 else 0))

        for i in range(num_messages):
            start_index = i * max_elements_per_message
            end_index = min((i + 1) * max_elements_per_message, num_elements)
            reply_data = {'template_type': 'generic', 'elements': elements[start_index:end_index]}
            send_generic_message(sender_id, reply_data)

    else:
        reply = f"Failed to get response from weather website. Status code: {status_code}"
        bot.send_text_message(sender_id, reply)


def send_generic_message(sender_id, query):
    """
    Function to send message in generic message
    """
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'recipient': {'id': sender_id},
        'message': {'attachment': {'type': 'template', 'payload': query}}
    }
    ENDPOINT = f"https://graph.facebook.com/v19.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    response = requests.post(ENDPOINT, headers=headers, json=data)
    log(response.json())


if __name__ == '__main__':
    app.run(debug=True, port=40)