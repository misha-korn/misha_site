state = {}


def arifmetic_operations_div_mult(
    calc_actions_div_multi, calc_actions, calc_numbers_lst
):
    # Умножение и деление должно быть в приоритете
    # print(calc_numbers_lst, 'calc_numbers_lst1')
    num_div_mult = 0
    for i in range(len(calc_actions_div_multi)):
        if (
            calc_numbers_lst[calc_actions_div_multi[i]]
            and calc_numbers_lst[calc_actions_div_multi[i] + 1]
        ):
            num_div_mult = arithmetic_operations(
                calc_numbers_lst[calc_actions_div_multi[i]],
                calc_numbers_lst[calc_actions_div_multi[i] + 1],
                calc_actions[calc_actions_div_multi[i]],
            )
            # print(calc_numbers_lst[calc_actions_div_multi[i] + 1], calc_actions[calc_actions_div_multi[i]],
            #       calc_numbers_lst[calc_actions_div_multi[i]])
            # print(num_div_mult, 'num_div_mult1')
            calc_numbers_lst[calc_actions_div_multi[i]] = None
            calc_actions[calc_actions_div_multi[i]] = None
            j = 0
            while j < len(calc_actions):
                sokr_biggest = sokrashenie_biggest(num_div_mult[1], num_div_mult[2])
                num_div_mult[1], num_div_mult[2] = (
                    int(sokr_biggest[0]),
                    int(sokr_biggest[1]),
                )
                j += 1
            if num_div_mult[3] == "-":
                calc_numbers_lst[calc_actions_div_multi[i] + 1] = [
                    num_div_mult[0],
                    num_div_mult[1],
                    num_div_mult[2],
                    False,
                ]
            else:
                calc_numbers_lst[calc_actions_div_multi[i] + 1] = [
                    num_div_mult[0],
                    num_div_mult[1],
                    num_div_mult[2],
                    True,
                ]
    # print(calc_numbers_lst, 'calc_numbers_lst2')
    # print(num_div_mult, 'num_div_mult2')
    calc_numbers_lst_copy = calc_numbers_lst.copy()
    calc_actions_copy = calc_actions.copy()
    calc_numbers_lst = []
    calc_actions = []
    for i in range(len(calc_numbers_lst_copy)):
        if calc_numbers_lst_copy[i]:
            calc_numbers_lst.append(calc_numbers_lst_copy[i])
    for i in range(len(calc_actions_copy)):
        if calc_actions_copy[i]:
            calc_actions.append(calc_actions_copy[i])
    # Все остальные арифметические действия
    if len(calc_actions) > 0:
        j = 0
        first_num = calc_numbers_lst[0]
        result = None
        while j < len(calc_actions):
            second_num = calc_numbers_lst[j + 1]
            result = arithmetic_operations(first_num, second_num, calc_actions[j])
            if result[3] == "-":
                first_num = [result[0], result[1], result[2], False]
            else:
                first_num = [result[0], result[1], result[2], True]
            sokr_biggest = sokrashenie_biggest(result[1], result[2])
            result[1], result[2] = int(sokr_biggest[0]), int(sokr_biggest[1])
            j += 1
        return result
    else:
        return num_div_mult


def arithmetic_operations(first_num, second_num, action):
    result = []
    first_num = checking_for_positivity(first_num)
    second_num = checking_for_positivity(second_num)
    if action == "+":
        if first_num[3] and second_num[3]:
            result = addition(first_num, second_num)
        elif first_num[3]:
            result = subtraction(first_num, second_num)
            if not bigger_smaller(first_num, second_num):
                result[3] = "-"
        elif second_num[3]:
            result = subtraction(first_num, second_num)
            if bigger_smaller(first_num, second_num):
                result[3] = "-"
        else:
            result = addition(first_num, second_num)
            result[3] = "-"
    elif action == "-":
        if first_num[3] and second_num[3]:
            result = subtraction(first_num, second_num)
            if not bigger_smaller(first_num, second_num):
                result[3] = "-"
        elif first_num[3]:
            result = addition(first_num, second_num)
        elif second_num[3]:
            result = addition(first_num, second_num)
            result[3] = "-"
        else:
            result = subtraction(first_num, second_num)
            if bigger_smaller(first_num, second_num):
                result[3] = "-"
    elif action == "*":
        result = [
            0,
            (first_num[1] + first_num[0] * first_num[2])
            * (second_num[1] + second_num[0] * second_num[2]),
            first_num[2] * second_num[2],
            "",
        ]
        # print(result, 'result1')
        result = checking_for_positivity(result)
        # print(result, 'result2')
        if result[1] >= result[2]:
            result[0] += result[1] // result[2]
            result[1] -= result[2] * (result[1] // result[2])
        if (first_num[3] and not second_num[3]) or (not first_num[3] and second_num[3]):
            result[3] = "-"
    elif action in ["/", ":"]:
        result = [
            0,
            (first_num[1] + first_num[0] * first_num[2]) * (second_num[2]),
            (first_num[2]) * (second_num[1] + second_num[0] * second_num[2]),
            "",
        ]
        result = checking_for_positivity(result)
        if result[1] >= result[2]:
            result[0] += result[1] // result[2]
            result[1] -= result[2] * (result[1] // result[2])
        if (first_num[3] and not second_num[3]) or (not first_num[3] and second_num[3]):
            result[3] = "-"
    return result


def znam(num):
    return len(num.split("/")) == 1


def checking_for_positivity(result):
    if result[0] < 0:
        result[0] *= -1
    if result[1] < 0:
        result[1] *= -1
    return result


def error():
    raise IndexError


def bigger_smaller(first_num, second_num):
    first_num = checking_for_positivity(first_num)
    second_num = checking_for_positivity(second_num)
    return (first_num[0] * first_num[2] + first_num[1]) * second_num[2] > (
        second_num[0] * second_num[2] + second_num[1]
    ) * first_num[2]


def subtraction(first_num, second_num):
    first_num = checking_for_positivity(first_num)
    second_num = checking_for_positivity(second_num)
    result = [
        0,
        (first_num[0] * first_num[2] + first_num[1]) * second_num[2]
        - (second_num[0] * second_num[2] + second_num[1]) * first_num[2],
        first_num[2] * second_num[2],
        "",
    ]
    result = checking_for_positivity(result)
    if result[1] >= result[2]:
        result[0] += result[1] // result[2]
        result[1] -= result[2] * (result[1] // result[2])
    return result


def addition(first_num, second_num):
    first_num = checking_for_positivity(first_num)
    second_num = checking_for_positivity(second_num)
    result = [
        0,
        (first_num[0] * first_num[2] + first_num[1]) * second_num[2]
        + (second_num[0] * second_num[2] + second_num[1]) * first_num[2],
        first_num[2] * second_num[2],
        "",
    ]
    result = checking_for_positivity(result)
    if result[1] >= result[2]:
        result[0] += result[1] // result[2]
        result[1] -= result[2] * (result[1] // result[2])
    return result


def sokrashenie(result_1, result_2, s):
    i = 2
    while i <= (int(result_1) + 1):
        if result_2 % i == 0 and result_1 % i == 0:
            result_2 /= i
            result_1 /= i
            s += 2
        i += 1
    s -= 1
    return result_1, result_2, s


def sokrashenie_biggest(result_1, result_2):
    s = 2
    sokr = sokrashenie(result_1, result_2, s)
    result_1 = sokr[0]
    result_2 = sokr[1]
    s = sokr[2]
    while s > 1:
        sokr = sokrashenie(result_1, result_2, s)
        result_1 = sokr[0]
        result_2 = sokr[1]
        s = sokr[2]
    return result_1, result_2, s


def message_processing(text_calc):
    # error()
    # if state[update.effective_user.id]["dia_stat"] == 1:
    text_error = "К сожалению, мы не можем обработать эти числа.😢"
    try:
        # error()
        # Ввод
        lst = str(text_calc).split(" ")

        if len(lst) // 2 + 1 >= 200:
            raise IndexError
        # state[update.effective_user.id]["count_numbers"] = (
        #     1
        #     + lst.count("-")
        #     + lst.count("+")
        #     + lst.count("/")
        #     + lst.count(":")
        #     + lst.count("*")
        # )
        numbers_lst = []
        for i in range(len(lst)):
            if lst[i] not in ["+", "-", "/", ":", "*"]:
                numbers_lst.append(lst[i])

        actions_lst = []
        for i in range(len(lst)):
            if lst[i] in ["+", "-", "/", ":", "*"]:
                actions_lst.append(lst[i])
            else:
                actions_lst.append(None)

        len_numbers = []
        len_number = 0
        for i in range(len(actions_lst)):
            if actions_lst[i]:
                len_numbers.append(len_number - 1)
            else:
                len_number += 1
        len_numbers.append(len_number - 1)

        int_numbers_lst = [[] for i in range(len(len_numbers))]
        new_numbers_lst = [[] for i in range(len(len_numbers))]
        calc_numbers_lst = [[] for i in range(len(len_numbers))]
        calc_actions_div_multi = []
        calc_actions = []

        run = True
        o = 0
        for i in range(len(len_numbers)):
            run = True
            while o < len(numbers_lst) and run:
                new_numbers_lst[i].append(numbers_lst[o])
                if o == len_numbers[i]:
                    run = False
                o += 1

        for i in range(len(new_numbers_lst)):
            for j in range(len(new_numbers_lst[i])):
                if znam(new_numbers_lst[i][j]):
                    int_numbers_lst[i].append(new_numbers_lst[i][j])
                else:
                    int_numbers_lst[i].append(new_numbers_lst[i][j].split("/")[0])
                    int_numbers_lst[i].append(new_numbers_lst[i][j].split("/")[1])

        for i in range(len(new_numbers_lst)):
            if len(int_numbers_lst[i]) == 3:
                calc_numbers_lst[i] = [
                    int_numbers_lst[i][0],
                    int_numbers_lst[i][1],
                    int_numbers_lst[i][2],
                    "",
                ]
            elif len(int_numbers_lst[i]) == 1:
                if not len(int_numbers_lst[i][0].split(".")) == 2:
                    calc_numbers_lst[i] = [int_numbers_lst[i][0], "0", "1", ""]
                else:
                    decimal_part = 1
                    for j in range(
                        len(
                            str(
                                int_numbers_lst[i][0]
                                .split(".")[1]
                                .replace(")", "", 1)
                                .replace("(", "", 1)
                            )
                        )
                    ):
                        decimal_part *= 10
                    calc_numbers_lst[i] = [
                        int_numbers_lst[i][0].split(".")[0],
                        int_numbers_lst[i][0].split(".")[1],
                        str(decimal_part),
                        "",
                    ]
            elif len(int_numbers_lst[i]) == 2:
                calc_numbers_lst[i] = [
                    "0",
                    int_numbers_lst[i][0],
                    int_numbers_lst[i][1],
                    "",
                ]
            if calc_numbers_lst[i][0][0] == "-" or calc_numbers_lst[i][1][0] == "-":
                calc_numbers_lst[i][3] = False
            else:
                calc_numbers_lst[i][3] = True

        left_brokes = 0
        right_brokes = 0
        problem = False
        brokes = [[] for i in range(len(calc_numbers_lst))]
        # print(calc_numbers_lst, 'calc_numbers_lst1')
        # print(int_numbers_lst, 'int_numbers_lst')

        for i in range(len(calc_numbers_lst)):
            calc_number = calc_numbers_lst[i]
            for j in range(len(calc_number) - 1):
                while "(" in calc_number[j]:
                    left_brokes += 1
                    calc_number[j] = calc_number[j].replace("(", "", 1)
                    brokes[i].append("(")
                while ")" in calc_number[j]:
                    right_brokes += 1
                    calc_number[j] = calc_number[j].replace(")", "", 1)
                    brokes[i].append(")")

            if "-" in [calc_number[0][0], calc_number[1][0]]:
                calc_numbers_lst[i] = [
                    calc_number[0],
                    calc_number[1],
                    calc_number[2],
                    False,
                ]
            else:
                calc_numbers_lst[i] = [
                    calc_number[0],
                    calc_number[1],
                    calc_number[2],
                    True,
                ]
        # print(calc_numbers_lst, 'calc_numbers_lst2')

        calc_numbers_brokes = []
        calc_index_brokes = []
        calc_actions_brokes = []
        last_original_numbers_broke = []
        last_previos_numbers_broke = []
        count_brokes = 0
        count_brokes_problem = 0
        last_count_brokes = 0
        max_count_brokes = 0
        for i in range(len(brokes)):
            index_brokes = 0
            for broke_in_broke in brokes[i]:
                if broke_in_broke == "(":
                    max_count_brokes += 1
                    count_brokes = max_count_brokes
                    brokes[i][index_brokes] = max_count_brokes
                    count_brokes_problem += 1
                    last_original_numbers_broke.append(max_count_brokes)
                elif broke_in_broke == ")":
                    while count_brokes in last_previos_numbers_broke:
                        count_brokes -= 1
                    brokes[i][index_brokes] = count_brokes
                    last_previos_numbers_broke.append(count_brokes)
                    count_brokes -= 1
                    count_brokes_problem -= 1
                index_brokes += 1
        if count_brokes_problem != 0:
            problem = True
        p = 0
        for i in range(len(actions_lst)):
            if actions_lst[i]:
                calc_actions.append(actions_lst[i])
                if actions_lst[i] in ["*", "/", ":"]:
                    calc_actions_div_multi.append(p)
                p += 1

        for i in range(len(brokes)):
            for count_in_brokes in brokes[i]:
                if count_in_brokes > last_count_brokes:
                    last_count_brokes = count_in_brokes
                    calc_number = [
                        [
                            int(calc_numbers_lst[i][0]),
                            int(calc_numbers_lst[i][1]),
                            int(calc_numbers_lst[i][2]),
                            calc_numbers_lst[i][3],
                        ]
                    ]
                    calc_index = [i]
                    calc_action_broke = [calc_actions[i]]
                    run = True
                    j = 1
                    while run:
                        calc_number.append(
                            [
                                int(calc_numbers_lst[i + j][0]),
                                int(calc_numbers_lst[i + j][1]),
                                int(calc_numbers_lst[i + j][2]),
                                calc_numbers_lst[i + j][3],
                            ]
                        )
                        calc_index.append(i + j)
                        z = 0
                        while z < len(brokes[i + j]):
                            if last_count_brokes == brokes[i + j][z]:
                                run = False
                            z += 1
                        if run:
                            calc_action_broke.append(calc_actions[i + j])
                            j += 1
                    calc_numbers_brokes.append(calc_number)
                    calc_index_brokes.append(calc_index)
                    calc_actions_brokes.append(calc_action_broke)

        for i in range(len(calc_numbers_lst)):
            calc_numbers_lst[i] = [
                int(calc_numbers_lst[i][0]),
                int(calc_numbers_lst[i][1]),
                int(calc_numbers_lst[i][2]),
                calc_numbers_lst[i][3],
            ]
            calc_numbers_lst[i] = checking_for_positivity(calc_numbers_lst[i])

        # Арифметические действия
        # print(calc_numbers_brokes, 'calc_numbers_brokes')
        # print(calc_actions_brokes, 'calc_actions_brokes')
        # print(calc_index_brokes, 'calc_index_brokes')
        # calc_actions_brokes_copy = calc_actions_brokes.copy()

        if not problem:
            for i in range(len(calc_numbers_lst)):
                if (
                    calc_numbers_lst[i][0] >= 1000000000000000000000000000
                    or calc_numbers_lst[i][2] >= 100000
                    or calc_numbers_lst[i][1] >= 100000
                ):
                    problem = True

        if problem:
            # await context.bot.send_message(
            #     chat_id=update.effective_chat.id,
            #     text="Числитель, знаменатель или целая часть введённых вами чисел слишком большая...",
            # )
            answer = "Числитель, знаменатель или целая часть введённых вами чисел слишком большая..."
            raise IndexError
        else:
            # Нужно учитывать скобки
            inverted_calc_numbers_brokes = []  # Переворачиваем списки
            for i in range(len(calc_numbers_brokes)):
                inverted_calc_numbers_brokes.append(calc_numbers_brokes[-i - 1])
            calc_numbers_brokes = inverted_calc_numbers_brokes

            inverted_calc_actions_brokes = []
            for i in range(len(calc_actions_brokes)):
                inverted_calc_actions_brokes.append(calc_actions_brokes[-i - 1])
            calc_actions_brokes = inverted_calc_actions_brokes

            inverted_calc_index_brokes = []
            for i in range(len(calc_index_brokes)):
                inverted_calc_index_brokes.append(calc_index_brokes[-i - 1])
            calc_index_brokes = inverted_calc_index_brokes

            calc_index_brokes_the_last_element = []

            for i in range(len(calc_numbers_lst)):
                calc_index_brokes_the_last_element.append(i)

            calc_numbers_brokes.append(calc_numbers_lst)
            calc_actions_brokes.append(calc_actions)
            calc_index_brokes.append(calc_index_brokes_the_last_element)

            # print(calc_numbers_brokes, 'calc_numbers_brokes')
            # print(calc_actions_brokes, 'calc_actions_brokes')
            # print(calc_index_brokes, 'calc_index_brokes')

            calc_numbers_brokes_results = []
            last_index_brokes = []

            for i in range(len(calc_numbers_brokes)):
                replacement = 0
                count_elements_vstr_many = []
                number_replacement_many = []
                index_replacement_many_f = []
                index_replacement_many_s = []

                for j in range(
                    len(last_index_brokes)
                ):  # Считаем количество повторений в скобках
                    not_replacement = True
                    count_elements_vstr = 0
                    number_replacement = []
                    index_replacement_f = []
                    index_replacement_s = []
                    for q in range(len(last_index_brokes[j])):
                        if last_index_brokes[j][q] in calc_index_brokes[i]:
                            count_elements_vstr += 1  # Количество повторов
                            number_replacement.append(
                                calc_index_brokes[i].index(last_index_brokes[j][q])
                            )  # Индексы повторяющихся элементов
                            index_replacement_f.append(j)
                            index_replacement_s.append(
                                calc_index_brokes[i].index(last_index_brokes[j][q])
                            )

                    if count_elements_vstr == len(last_index_brokes[j]):
                        for q in range(len(last_index_brokes)):
                            if (
                                len(last_index_brokes[j]) < len(last_index_brokes[q])
                                and last_index_brokes[j][0] in last_index_brokes[q]
                            ):
                                not_replacement = False
                        if not_replacement:
                            replacement += 1  # Количество повторений в скобках
                            count_elements_vstr_many.append(
                                count_elements_vstr
                            )  # Список количеств повторов
                            number_replacement_many.append(
                                number_replacement
                            )  # Список индексов повторяющихся элементов
                            index_replacement_many_f.append(
                                index_replacement_f
                            )  # Список индексов изначальных элементов
                            index_replacement_many_s.append(
                                index_replacement_s
                            )  # Список индексов заменяющих элементов
                            # print(last_index_brokes[j], calc_index_brokes[i], 'last_index_brokes[j], calc_index_brokes[i]')
                # print(replacement, 'replacement')
                # print(count_elements_vstr_many, 'count_elements_vstr_many')
                # print(index_replacement_many_f, 'index_replacement_many_f')
                # print(index_replacement_many_s, 'index_replacement_many_s')

                for j in range(replacement):  # Делаем замены
                    num_replace = 0  # Номер замены
                    for q in range(count_elements_vstr_many[j]):
                        # print(calc_numbers_brokes)
                        # print(calc_actions_brokes)
                        if (
                            num_replace == 0
                        ):  # Если замена 1, то он заменяет на результат нужной скобки
                            calc_numbers_brokes[i][index_replacement_many_s[j][q]] = (
                                calc_numbers_brokes_results
                            )[index_replacement_many_f[j][q]]

                        else:  # Если замена не 1, то он заменяет на None
                            calc_numbers_brokes[i][index_replacement_many_s[j][q]] = (
                                None
                            )
                        num_replace += 1

                    # Настройка actions
                    for m in range(
                        len(number_replacement_many[j]) - 1
                    ):  # Количество заменяемых элементов - 1
                        calc_actions_brokes[i][index_replacement_many_s[j][m]] = None

                new_calc_numbers_brokes = []  # Отчистка от None чисел
                for m in range(len(calc_numbers_brokes[i])):
                    if calc_numbers_brokes[i][m] != None:
                        new_calc_numbers_brokes.append(calc_numbers_brokes[i][m])
                calc_numbers_brokes[i] = new_calc_numbers_brokes

                new_calc_actions_brokes = []  # Отчистка от None действий
                for m in range(len(calc_actions_brokes[i])):
                    if calc_actions_brokes[i][m] != None:
                        new_calc_actions_brokes.append(calc_actions_brokes[i][m])
                calc_actions_brokes[i] = new_calc_actions_brokes

                # print(calc_numbers_brokes)
                # print(calc_actions_brokes)
                # print(calc_numbers_brokes_results)

                calc_actions_div_multi_broke = []  # Создание calc_actions_div_multi_broke
                p = 0
                for symbol in calc_actions_brokes[i]:
                    if symbol in ["*", "/", ":"]:
                        calc_actions_div_multi_broke.append(p)
                    p += 1

                last_result_broke = arifmetic_operations_div_mult(
                    calc_actions_div_multi_broke,
                    calc_actions_brokes[i],
                    calc_numbers_brokes[i],
                )
                if last_result_broke[3] == "-":
                    last_result_broke[3] = False
                elif last_result_broke[3] == "":
                    last_result_broke[3] = True
                last_index_brokes.append(calc_index_brokes[i])
                calc_numbers_brokes_results.append(last_result_broke)

            # print(calc_numbers_brokes_results, 'calc_numbers_brokes_results')

            # result = arifmetic_operations_div_mult(calc_actions_div_multi, calc_actions, calc_numbers_lst)
            result = calc_numbers_brokes_results[-1]
            if result[3]:
                result[3] = ""
            else:
                result[3] = "-"

            if int(result[1]) >= 5000000:
                answer = (
                    f"Мы не можем сократить полученый нами результат, "
                    f"т.к числитель или знаменатель вводных чисел слишком большой."
                    f"Однако мы можем сказать вам не сокращенную дробь. {result[3]}{result[0]} {result[1]}/{result[2]}"
                )
                # await context.bot.send_message(
                #     chat_id=update.effective_chat.id, text=text
                # )
            else:
                sokr_biggest = sokrashenie_biggest(result[1], result[2])
                result[1], result[2] = sokr_biggest[0], sokr_biggest[1]
                if int(result[1]) == 0:
                    text = f"{result[3]}{result[0]}"
                else:
                    text = f"{result[3]}{result[0]} {int(result[1])}/{int(result[2])}"
                # await context.bot.send_message(
                #     chat_id=update.effective_chat.id, text=text
                # )
                answer = text
                return answer
    except IndexError:
        # await context.bot.send_message(
        #     chat_id=update.effective_chat.id, text=text_error
        # )
        answer = text_error
        # print(IndexError)
    except TypeError:
        # await context.bot.send_message(
        #     chat_id=update.effective_chat.id, text=text_error
        # )
        answer = text_error
        # print(TypeError)
    except ValueError:
        # await context.bot.send_message(
        #     chat_id=update.effective_chat.id, text=text_error
        # )
        answer = text_error
        # print(ValueError)
    except ZeroDivisionError:
        # await context.bot.send_message(
        #     chat_id=update.effective_chat.id, text=text_error
        # )
        answer = text_error
        # print(ZeroDivisionError)
    except OverflowError:
        # await context.bot.send_message(
        #     chat_id=update.effective_chat.id, text=text_error
        # )
        answer = text_error
        # print(OverflowError)
    finally:
        return answer
