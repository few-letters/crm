def get_calculator(operator):
    # Ця функція повертає "маленьку" функцію залежно від знака
    if operator == "+":
        def add(a, b): return a + b
        return add
    elif operator == "*":
        def multiply(a, b): return a * b
        return multiply

# --- Спосіб 1 (Класичний) ---
calc_func = get_calculator("*")  # Отримуємо функцію множення
result = calc_func(5, 10)        # Викликаємо її
print(result) # 50

# --- Спосіб 2 (Ланцюговий - те, що тебе здивувало) ---
# Ми викликаємо першу функцію, вона повертає об'єкт,
# і ми ТУТ ЖЕ ставимо дужки, щоб викликати цей об'єкт.
print( get_calculator("*")(5, 10) )  # 50

def simple_func(text):
    print(text)
    return 'text'

simple_func('123')('456')