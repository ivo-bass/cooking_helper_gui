import webbrowser
from calendar import day_name
from csv import writer, reader
from datetime import datetime, timedelta
from random import randrange
from time import sleep

from easygui import buttonbox, msgbox

from cooking_lists import *
from questions import *

version = "Cooking Helper v.1"


def get_datetime():
    """Тази функция връща всички променливи свързани с дати и часове"""
    get_date_and_time = datetime.now()
    current_date = get_date_and_time.strftime("%d/%m/%Y")
    current_time = get_date_and_time.strftime("%H:%M")
    current_hour = get_date_and_time.strftime("%H")
    current_day = day_name[datetime.strptime(current_date, '%d/%m/%Y').weekday()]
    get_tomorrow_date = get_date_and_time + timedelta(days=1)
    tomorrow_date = get_tomorrow_date.strftime("%d/%m/%Y")

    # Не много умен начин да преведа на български дните от седмицата
    if current_day == "Monday":
        current_day = "понеделник"
    elif current_day == "Tuesday":
        current_day = "вторник"
    elif current_day == "Wednesday":
        current_day = "сряда"
    elif current_day == "Thursday":
        current_day = "четвъртък"
    elif current_day == "Friday":
        current_day = "петък"
    elif current_day == "Saturday":
        current_day = "събота"
    elif current_day == "Sunday":
        current_day = "неделя"
    return current_date, current_time, current_hour, current_day, tomorrow_date


def greetings():
    """Функция, която отправя елементарен поздрав в зависимост от часа на стартиране на програмата
    и задава'приятелски' въпрос от типа 'Как си днес?'"""
    current_hour = get_datetime()[2]
    if 1 <= int(current_hour) < 12:
        greeting = "Добро утро"
        question = morning_questions[randrange(0, len(morning_questions))]
    elif 12 <= int(current_hour) < 18:
        greeting = "Добър ден"
        question = afternoon_questions[randrange(0, len(afternoon_questions))]
    elif 18 <= int(current_hour) < 21:
        greeting = "Добър вечер"
        question = evening_questions[randrange(0, len(evening_questions))]
    else:
        greeting = "Добър вечер"
        question = night_questions[randrange(0, len(night_questions))]
    return greeting, question


def main_coarse_suggestion_func():
    """Функция, която връща предложение за основно ястие.
    Първо съобразява, че ако е събота или неделя, трябва да се сготви нещо, което може да го яде Ангел.
    След това добавя гарнитура към основното, ако то има нужда от такава.
    А ако гарнитурата се падне да бъде салата, я избира от списък със салати."""
    current_day = get_datetime()[3]
    if current_day in ("събота", "неделя"):
        main_coarse_suggestion = child_list[randrange(0, len(child_list))]
    else:
        main_coarse_suggestion = main_dish_list[randrange(0, len(main_dish_list))]
    if main_coarse_suggestion in garnish_needed:
        garnish_suggestion = garnish_list[randrange(0, len(garnish_list))]
        if garnish_suggestion == "салата":
            garnish_suggestion = salad_list[randrange(0, len(salad_list))]
        main_coarse_suggestion = main_coarse_suggestion + " с " + garnish_suggestion
    return main_coarse_suggestion


def breakfast_suggestion_func():
    """Връща предложение за закуска."""
    breakfast_suggestion = breakfast_list[randrange(0, len(breakfast_list))]
    return breakfast_suggestion


def salad_suggestion_func():
    """Връща предложение за салата."""
    salad_suggestion = salad_list[randrange(0, len(salad_list))]
    return salad_suggestion


def dessert_suggestion_func():
    """Връща предложение за десерт."""
    dessert_suggestion = dessert_list[randrange(0, len(dessert_list))]
    return dessert_suggestion


def order_func():
    """Връща предложение за поръчка на храна онлайн."""
    order_food = order_list[randrange(0, len(order_list))]
    return order_food


def file_write_func(date, food_suggestion):
    """Записва дата и избрано ястие в CSV файл."""
    file = open("history.csv", 'a+', newline='', encoding='utf-8')
    row = (date, food_suggestion)
    write_csv = writer(file)
    write_csv.writerow(row)
    file.close()


def file_read_func():
    """Чете от файла с историята на одобрените ястия и връща списък с избраните за текущия ден ястия."""
    file = open("history.csv", 'r', newline='', encoding='utf-8')
    read_csv = reader(file, delimiter=',')
    dates = []
    foods_for_today = []
    current_date = get_datetime()[0]
    for row in read_csv:
        dates.append(row[0])
        if row[0] == current_date:
            foods_for_today.append(row[1])
    file.close()
    return dates, foods_for_today


def takeaway_open_func():
    """Отваря интернет страницата на Тейкауей."""
    web_address = "https://www.takeaway.com/bg/"
    webbrowser.open(web_address)


def if_nothing_selected_func():
    """Функция, която извиква, когато от всички позволени превъртания на
    циклите за предложение на храна, не е избрано нито едно ястие.
    Позволява 1 предложение за онлайн поръчка на храна и отваря страницата на Тейкауей."""
    order_food = order_func()
    current_date = get_datetime()[0]
    msg = f"Очевидно днес не ти се готви." \
          f"\nПредлагам ти тогава, {order_food}." \
          f"\nСъгласна ли си?"
    options = ["ДА", "НЕ"]
    order_prompt = buttonbox(msg=msg, title=version, choices=options)
    if order_prompt == "ДА":
        file_write_func(current_date, order_food)
        msgbox("Добре, отварям за теб www.takeaway.com...", title=version)
        sleep(2)
        takeaway_open_func()
        end_page()
    elif order_food == "НЕ":
        msgbox("Хм... Мисля, че е по-добре да си починеш малко.", title=version)
        end_page()
    else:
        out_msg()


def check_receipt_in_google(food_suggestion):
    """Отваря google.com със зададено търсене на рецепта за конкретно ястие."""
    search = "рецепта за " + food_suggestion
    webbrowser.open("http://google.com/?#q=" + search)


def foods_for_last_week_func():
    """Тази функция чете данните от файла с историята
    и ни връща списък с всички избрани храни за последнитата седмица."""
    last_week_dates_list = []
    for n in range(1, 7):
        date_n_days_ago = datetime.now() - timedelta(days=n)
        date_n_days_ago = date_n_days_ago.strftime("%d/%m/%Y")
        last_week_dates_list.append(date_n_days_ago)
    file = open("history.csv", 'r', newline='', encoding='utf-8')
    read_csv = reader(file, delimiter=',')
    dates = []
    foods_for_week_list = []
    for row in read_csv:
        dates.append(row[0])
        if row[0] in last_week_dates_list:
            foods_for_week_list.append(row[1])
    file.close()
    return foods_for_week_list


"""_______________________НОВИ ФУНКЦИИ ЗА GUI__________________________"""


def home_page():
    greeting = greetings()[0]
    current_day = get_datetime()[3]
    current_time = get_datetime()[1]
    current_date = get_datetime()[0]
    foods_for_today = file_read_func()[1]
    foods_for_today_string = ', '.join(foods_for_today)
    dates_saved = file_read_func()[0]
    if current_date in dates_saved:
        start_msg = f"\nЗа днес вече си избрала {foods_for_today_string.upper()}."
        start_prompt = "\nИскаш ли да сготвим още нещо?"
    else:
        start_msg = f"\nЗа днес все още не си избрала ястие."
        start_prompt = "\nИскаш ли да избереш какво да сготвим?"
    hello_msg = f"{greeting}, скъпа!" \
                f"\nДнес е {current_day}, часът е: {current_time}" \
                f"\n{greetings()[1]}" \
                f"\n\n{start_msg}" \
                f"\n{start_prompt}"
    start_options = ["ДА", "НЕ"]
    start = buttonbox(msg=hello_msg, title=version, choices=start_options)
    if start == start_options[0]:
        choose_coarse()
    elif start == start_options[1]:
        msgbox("\nОК. Когато ти потрябвам, знаеш къде да ме намериш.\nЧао!")
    else:
        out_msg()


def choose_coarse():
    choose_button = buttonbox("\nКакво искаш да ти предложа?", title=version, choices=coarse_options_list)
    if choose_button == coarse_options_list[0]:
        main_coarse()
    elif choose_button == coarse_options_list[1]:
        salad()
    elif choose_button == coarse_options_list[2]:
        dessert()
    elif choose_button == coarse_options_list[3]:
        breakfast()
    elif choose_button == coarse_options_list[4]:
        end_page()
    else:
        out_msg()


def main_coarse():
    current_date = get_datetime()[0]
    denied_list = []
    denied_list_string = ', '.join(denied_list)
    foods_for_today = file_read_func()[1]
    foods_for_today_string = ', '.join(foods_for_today)
    foods_for_last_week = foods_for_last_week_func()
    foods_for_last_week_string = ', '.join(foods_for_last_week)
    main_coarse_suggestion = ""
    for _ in range(10):
        if "риба" not in foods_for_last_week_string \
                and "риба" not in foods_for_today_string \
                and "риба" not in denied_list_string \
                and len(foods_for_last_week) > 0:
            msg = "От доста време не сме готвили риба. Искаш ли риба за днес?"
            options = ["ДА", "НЕ"]
            fish_prompt = buttonbox(msg=msg, title=version, choices=options)
            if fish_prompt == "ДА":
                main_coarse_suggestion = "риба"
            else:
                denied_list.append("риба")

        while main_coarse_suggestion != "риба":
            main_coarse_suggestion = main_coarse_suggestion_func()
            if main_coarse_suggestion in denied_list_string \
                    or main_coarse_suggestion in foods_for_last_week_string\
                    or main_coarse_suggestion in foods_for_today_string:
                main_coarse_suggestion = main_coarse_suggestion_func()
            else:
                break

        msg = f"\nДнес може да сготвим {main_coarse_suggestion.upper()}." \
              f"\nСъгласна ли си с това предложение?"
        options = ["ДА", "НЕ"]
        main_coarse_prompt = buttonbox(msg=msg, title=version, choices=options)
        if main_coarse_prompt == "ДА":
            file_write_func(current_date, main_coarse_suggestion)
            msg = f"\nУра! Ще готвим {main_coarse_suggestion}. Знам, че ще бъде много вкусно!"
            options = ["ПРОДЪЛЖИ", "РЕЦЕПТА В GOOGLE", "ИЗХОД"]
            next_step = buttonbox(msg=msg, title=version, choices=options)
            if next_step == "РЕЦЕПТА В GOOGLE":
                check_receipt_in_google(main_coarse_suggestion)
                end_page()
                break
            elif next_step == "ПРОДЪЛЖИ":
                choose_coarse()
                break
            elif next_step == "ИЗХОД":
                end_page()
                break
            else:
                break
        elif main_coarse_prompt == "НЕ":
            denied_list.append(main_coarse_suggestion)
        else:
            break
    else:
        if_nothing_selected_func()


def salad():
    current_date = get_datetime()[0]
    foods_for_last_week = foods_for_last_week_func()
    foods_for_today = file_read_func()[1]
    denied_list = []
    for _ in range(5):
        while True:
            salad_suggestion = salad_suggestion_func()
            if salad_suggestion in denied_list \
                    or salad_suggestion in foods_for_last_week \
                    or salad_suggestion in foods_for_today:
                salad_suggestion = salad_suggestion_func()
            else:
                break
        msg = f"\nСалатката ни днес може да бъде {salad_suggestion.upper()}." \
              f"\nСъгласна ли си с това предложение?"
        options = ["ДА", "НЕ"]
        choose_salad = buttonbox(msg=msg, title=version, choices=options)
        if choose_salad == "ДА":
            file_write_func(current_date, salad_suggestion)
            msg = f"\nУра! Ще готвим {salad_suggestion}. Знам, че ще бъде много вкусно!"
            options = ["ПРОДЪЛЖИ", "РЕЦЕПТА В GOOGLE", "ИЗХОД"]
            next_step = buttonbox(msg=msg, title=version, choices=options)
            if next_step == "РЕЦЕПТА В GOOGLE":
                check_receipt_in_google(salad_suggestion)
                end_page()
                break
            elif next_step == "ПРОДЪЛЖИ":
                choose_coarse()
                break
            elif next_step == "ИЗХОД":
                end_page()
                break
            else:
                break
        elif choose_salad == "НЕ":
            denied_list.append(salad_suggestion)
        else:
            break
    else:
        msgbox("\nНе успя да си харесаш нищо...", title=version)
        home_page()


def dessert():
    current_date = get_datetime()[0]
    foods_for_last_week = foods_for_last_week_func()
    foods_for_today = file_read_func()[1]
    denied_list = []
    for _ in range(5):
        while True:
            dessert_suggestion = dessert_suggestion_func()
            if dessert_suggestion in denied_list \
                    or dessert_suggestion in foods_for_last_week\
                    or dessert_suggestion in foods_for_today:
                dessert_suggestion = dessert_suggestion_func()
            else:
                break

        msg = f"\nДнес за десерт можем да имаме {dessert_suggestion.upper()}." \
              f"\nСъгласна ли си с това предложение?"
        options = ["ДА", "НЕ"]
        choose_dessert = buttonbox(msg=msg, title=version, choices=options)
        if choose_dessert == "ДА":
            file_write_func(current_date, dessert_suggestion)
            msg = f"\nУра! Ще се подсладим с {dessert_suggestion}. Знам, че ще бъде много вкусно!"
            options = ["ПРОДЪЛЖИ", "РЕЦЕПТА В GOOGLE", "ИЗХОД"]
            next_step = buttonbox(msg=msg, title=version, choices=options)
            if next_step == "РЕЦЕПТА В GOOGLE":
                check_receipt_in_google(dessert_suggestion)
                end_page()
                break
            elif next_step == "ПРОДЪЛЖИ":
                choose_coarse()
                break
            elif next_step == "ИЗХОД":
                end_page()
                break
            else:
                break
        elif choose_dessert == "НЕ":
            denied_list.append(dessert_suggestion)
        else:
            break
    else:
        msgbox("\nНе успя да си харесаш нищо...", title=version)
        home_page()


def breakfast():
    current_date = get_datetime()[0]
    tomorrow_date = get_datetime()[4]
    foods_for_last_week = foods_for_last_week_func()
    foods_for_today = file_read_func()[1]
    denied_list = []
    for _ in range(5):
        while True:
            breakfast_suggestion = breakfast_suggestion_func()
            if breakfast_suggestion in denied_list \
                    or breakfast_suggestion in foods_for_last_week \
                    or breakfast_suggestion in foods_for_today:
                breakfast_suggestion = breakfast_suggestion_func()
            else:
                break
        msg = f"\nКакво ще кажеш за {breakfast_suggestion.upper()}?" \
              f"\nСъгласна ли си с това предложение?"
        options = ["ДА", "НЕ"]
        breakfast_prompt = buttonbox(msg=msg, title=version, choices=options)
        if breakfast_prompt == "ДА":
            msg = f"{breakfast_suggestion.upper()} - за днес или за утре ще бъде?"
            options = ["ЗА ДНЕС", "ЗА УТРЕ"]
            choose_day = buttonbox(msg=msg, title=version, choices=options)
            if choose_day == "ЗА ДНЕС":
                file_write_func(current_date, breakfast_suggestion)
                msg = f"\nДнес ще закусваме {breakfast_suggestion}. Ммм...Вкусно!"
                options = ["ПРОДЪЛЖИ", "РЕЦЕПТА В GOOGLE", "ИЗХОД"]
                next_step = buttonbox(msg=msg, title=version, choices=options)
                if next_step == "РЕЦЕПТА В GOOGLE":
                    check_receipt_in_google(breakfast_suggestion)
                    end_page()
                    break
                elif next_step == "ПРОДЪЛЖИ":
                    choose_coarse()
                    break
                elif next_step == "ИЗХОД":
                    end_page()
                    break
                else:
                    break
            elif choose_day == "ЗА УТРЕ":
                file_write_func(tomorrow_date, breakfast_suggestion)
                msg = f"\nУтре ще закусваме {breakfast_suggestion}. Ммм...Вкусно!"
                options = ["ПРОДЪЛЖИ", "РЕЦЕПТА В GOOGLE", "ИЗХОД"]
                next_step = buttonbox(msg=msg, title=version, choices=options)
                if next_step == "РЕЦЕПТА В GOOGLE":
                    check_receipt_in_google(breakfast_suggestion)
                    end_page()
                    break
                elif next_step == "ПРОДЪЛЖИ":
                    choose_coarse()
                    break
                elif next_step == "ИЗХОД":
                    end_page()
                    break
                else:
                    break
        elif breakfast_prompt == "НЕ":
            denied_list.append(breakfast_suggestion)
        else:
            break
    else:
        msgbox("\nНе успя да си харесаш нищо...", title=version)
        home_page()


def end_page():
    foods_for_today = file_read_func()[1]
    foods_for_today_string = ', '.join(foods_for_today)
    if not foods_for_today:
        msg = "За днес няма избрани ястия."
    else:
        msg = f"\nСписъкът за днес е:" \
          f"\n{foods_for_today_string.upper()}"
    options = ["НАЧАЛО", "ИЗХОД"]
    next_step = buttonbox(msg=msg, title=version, choices=options)
    if next_step == "НАЧАЛО":
        home_page()
    elif next_step == "ИЗХОД":
        out_msg()


def out_msg():
    msgbox("\nЖелая ти прекрасен остатък от деня. Чао!", title=version)
