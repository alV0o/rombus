import customtkinter as ctk
import GetPoints
import GetProducts
import addStep
import json
import time

# 1. Настройка внешнего вида
ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")  

# 2. Создание главного окна
app = ctk.CTk()
app.title("Управление станциями и продуктами")
app.geometry("450x650") 
app.resizable(False, False)

# Инициализируем переменные дефолтными значениями, чтобы Tkinter не падал
all_maps = ["Нет карт"]
products_name = ["Нет товаров"]
pickup_names = ["Нет станций"]
dropoff_names = ["Нет станций"]
all_points = []
products = []

try:
    all_maps = GetPoints.get_api_maps()
    time.sleep(0.1)
    
    if all_maps:
        all_points = GetPoints.get_api_points(all_maps[0])
        print("Ok: Карты и точки успешно получены")
        
        products = GetProducts.GetProducts_()
        if products:
            products_name = [product[1] for product in products]
        
        pickup_names = [p["place_name"] for p in all_points if p["role"] == "pickup"]
        dropoff_names = [p["place_name"] for p in all_points if p["role"] == "dropoff"]

        # БЕЗОПАСНЫЙ КУСОК: проверяем длину перед обращением по индексу [1]
        if len(pickup_names) > 1:
            target_name = pickup_names[1]
            target_point = next((p for p in all_points if p["place_name"] == target_name), None)
            if target_point:
                print(target_point.get("handler", "unknown"))  
                print(target_point)  
        else:
            print("Предупреждение: В pickup_names меньше 2-х элементов. Пропускаем target_point.")
            
except Exception as e:
    print("Error во время инициализации: ", e)


def checkBox_Check():
    # По умолчанию скрываем инструкцию при запуске
    if not checkbox.get():
        frame_ws1.grid(row=3, column=0, padx=50, sticky="w")
        frame_ws2.grid(row=4, column=0, padx=50, sticky="w")
        frame_instr.grid_forget()
    else:
        frame_ws1.grid_forget()
        frame_ws2.grid_forget()
        frame_instr.grid(row=5, column=0, padx=50, sticky="w")


def button_click():
    name = entry_name.get()
    goods = combo_goods.get()
    
    # Защита на случай, если список продуктов пуст
    if products:
        products_dict = {prod[1]: prod[0] for prod in products}
        product_id = products_dict.get(goods)
    else:
        product_id = None
        
    addStep.AddStep(product_id, CreateInstruction(), name)


def CreateInstruction():
    selected_ws1 = combo_ws1.get()
    selected_ws2 = combo_ws2.get()

    # Ищем точки в глобальном массиве all_points
    pickup_point = next((p for p in all_points if p["place_name"] == selected_ws1), None)
    dropoff_point = next((p for p in all_points if p["place_name"] == selected_ws2), None)

    pickup_handler = pickup_point["handler"] if pickup_point else "unknown"
    dropoff_handler = dropoff_point["handler"] if dropoff_point else "unknown"

    data = {
        "task_id": "-1",
        "pickup": {"place_name": selected_ws1, "handler": pickup_handler},
        "dropoff": {"place_name": selected_ws2, "handler": dropoff_handler}, 
        "payload": {"sku": combo_goods.get(), "quantity": 5}
    }

    return json.dumps(data, ensure_ascii=False, indent=4)


# ИСПРАВЛЕНО: функция теперь принимает аргумент `choice` (его автоматически передает ComboBox)
def get_new_map(choice):
    global all_points # Объявляем глобальной, чтобы изменения записались для функции CreateInstruction
    try:
        new_points = GetPoints.get_api_points(choice)
        all_points = new_points # Обновляем глобальный список точек для новой карты
        
        new_pickups = [p["place_name"] for p in new_points if p["role"] == "pickup"]
        new_dropoffs = [p["place_name"] for p in new_points if p["role"] == "dropoff"]
        
        combo_ws1.configure(values=new_pickups if new_pickups else ["Нет станций"])
        combo_ws2.configure(values=new_dropoffs if new_dropoffs else ["Нет станций"])
        
        # Сбрасываем текст в комбобоксах на первый элемент из новых списков
        combo_ws1.set(new_pickups[0] if new_pickups else "Нет станций")
        combo_ws2.set(new_dropoffs[0] if new_dropoffs else "Нет станций")
    except Exception as e:
        print("Ошибка при смене карты:", e)


app.columnconfigure(0, weight=1)

label_top = ctk.CTkLabel(app, text="Добавление шага", font=("Arial", 18, "bold"))
label_top.grid(row=0, column=0, pady=20)

# --- Блок: Товар ---
frame_goods = ctk.CTkFrame(app, fg_color="transparent")
frame_goods.grid(row=1, column=0, padx=50, sticky="w")
app.rowconfigure(1, minsize=130)  # Увеличили minsize, так как внутри теперь два комбобокса

label_good = ctk.CTkLabel(frame_goods, text="Карта:", font=("Arial", 14))
label_good.pack(anchor="w")
# ИСПРАВЛЕНО: Передаем только имя функции, БЕЗ скобок `()`. Скобки вызывали функцию ДО старта интерфейса.
combo_good = ctk.CTkComboBox(frame_goods, values=all_maps, width=350, command=get_new_map)
combo_good.pack(anchor="w", pady=(2, 5))

label_goods = ctk.CTkLabel(frame_goods, text="Товар:", font=("Arial", 14))
label_goods.pack(anchor="w")
combo_goods = ctk.CTkComboBox(frame_goods, values=products_name, width=350)
combo_goods.pack(anchor="w", pady=(2, 0))

# --- Блок: Имя ---
frame_name = ctk.CTkFrame(app, fg_color="transparent")
frame_name.grid(row=2, column=0, padx=50, sticky="w")
app.rowconfigure(2, minsize=110)  

label_name = ctk.CTkLabel(frame_name, text="Текстовое поле 'Имя':", font=("Arial", 14))
label_name.pack(anchor="w")
entry_name = ctk.CTkEntry(frame_name, placeholder_text="Введите имя...", width=350)
entry_name.pack(anchor="w", pady=(2, 0))
checkbox = ctk.CTkCheckBox(frame_name, text="Опционально", width=350, command=checkBox_Check)
checkbox.pack(anchor="w", pady=(5, 0))

# --- Блок: Рабочие станции 1 ---
frame_ws1 = ctk.CTkFrame(app, fg_color="transparent")
frame_ws1.grid(row=3, column=0, padx=50, sticky="w")
app.rowconfigure(3, minsize=80)

label_ws1 = ctk.CTkLabel(frame_ws1, text="Рабочие станции (Откуда):", font=("Arial", 14))
label_ws1.pack(anchor="w")
combo_ws1 = ctk.CTkComboBox(frame_ws1, values=pickup_names, width=350)
combo_ws1.pack(anchor="w", pady=(2, 0))

# --- Блок: Рабочие станции 2 ---
frame_ws2 = ctk.CTkFrame(app, fg_color="transparent")
frame_ws2.grid(row=4, column=0, padx=50, sticky="w")
app.rowconfigure(4, minsize=80)

label_ws2 = ctk.CTkLabel(frame_ws2, text="Рабочие станции (Куда):", font=("Arial", 14))
label_ws2.pack(anchor="w")
combo_ws2 = ctk.CTkComboBox(frame_ws2, values=dropoff_names, width=350)
combo_ws2.pack(anchor="w", pady=(2, 0))

# --- Блок: Инструкция ---
frame_instr = ctk.CTkFrame(app, fg_color="transparent")
app.rowconfigure(5, minsize=60)
# ИСПРАВЛЕНО: Сразу скрываем этот фрейм при запуске скрипта, так как чекбокс по умолчанию выключен
frame_instr.grid_forget() 

instr = ctk.CTkEntry(frame_instr, placeholder_text="Введите инструкцию", width=350)
instr.pack(anchor="w")

# --- Блок: Продукт ---
frame_product = ctk.CTkFrame(app, fg_color="transparent")
frame_product.grid(row=6, column=0, padx=50, sticky="w")
app.rowconfigure(6, minsize=80)

label_product = ctk.CTkLabel(frame_product, text="Продукт:", font=("Arial", 14))
label_product.pack(anchor="w")
combo_product = ctk.CTkComboBox(frame_product, values=["Продукт 1", "Продукт 2", "Продукт 3"], width=350)
combo_product.pack(anchor="w", pady=(2, 0))

# --- Кнопка подтверждения ---
button = ctk.CTkButton(app, text="Подтвердить", width=200, height=40, font=("Arial", 14, "bold"), command=button_click)
button.grid(row=7, column=0, pady=20)

# Принудительно вызываем проверку состояния чекбокса на старте, чтобы выстроить сетку
checkBox_Check()

app.mainloop()