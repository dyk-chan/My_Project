import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox
import random

# Визначення ваг функціоналу за замовчуванням (можна змінювати для сценаріїв)
def get_weights(scenario=1):
    if scenario == 1:
        return {
            "POS-система": 20,
            "Облік запасів": 15,
            "Програма лояльності": 10,
            "Інтеграція з платіжними системами": 20,
            "Аналітика": 20,
            "Мобільний додаток": 10,
            "Оффлайн режим": 5
        }
    elif scenario == 2:
        return {
            "POS-система": 10,
            "Облік запасів": 10,
            "Програма лояльності": 15,
            "Інтеграція з платіжними системами": 10,
            "Аналітика": 30,
            "Мобільний додаток": 15,
            "Оффлайн режим": 10
        }
    elif scenario == 3:
        return {
            "POS-система": 10,
            "Облік запасів": 10,
            "Програма лояльності": 10,
            "Інтеграція з платіжними системами": 15,
            "Аналітика": 10,
            "Мобільний додаток": 25,
            "Оффлайн режим": 20
        }

# Дані по функціоналу ПС
systems_data = {
    "Poster":        [1, 1, 1, 1, 1, 1, 0],
    "Cashalot":      [1, 1, 0, 0, 1, 1, 1],
    "Syrve":         [1, 1, 1, 1, 1, 1, 0],
    "ULTRA Company": [1, 1, 0, 1, 1, 0, 1],
    "R-Keeper":      [1, 1, 1, 1, 1, 1, 0]
}

features = list(get_weights().keys())
df = pd.DataFrame(systems_data, index=features)

# Обчислення ефективності

def calculate_effectiveness(weights):
    weighted_df = df.mul(pd.Series(weights), axis=0)
    return weighted_df.sum().sort_values(ascending=False)

# Вивід графіку ефективності у вікні tkinter

def plot_effectiveness_in_window(eff, title, root):
    frame = tk.Toplevel(root)
    frame.title(title)
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=eff.values, y=eff.index, hue=eff.index, palette="viridis", legend=False, ax=ax)
    ax.set_title(title)
    ax.set_xlabel("Ефективність (%)")
    ax.set_xlim(0, 100)
    ax.grid(axis='x')
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both')
    tk.Button(frame, text="Закрити", command=frame.destroy).pack(pady=5)

# Теплова карта

def plot_heatmap_window(root):
    frame = tk.Toplevel(root)
    frame.title("Реалізація функціоналу в ПС")
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(df.T, annot=True, cmap="YlGnBu", cbar=False, linewidths=.5, ax=ax)
    ax.set_title("Реалізація функціоналу в ПС")
    ax.set_xlabel("Функціонали")
    ax.set_ylabel("Програмні системи")
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both')
    tk.Button(frame, text="Закрити", command=frame.destroy).pack(pady=5)

# Стрес-тест

def plot_stress_distribution_in_window(effectiveness_series, root):
    frame = tk.Toplevel(root)
    frame.title("Стрес-тест")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(effectiveness_series, bins=15, kde=True, ax=ax)
    ax.set_title("Стрес-тест: розподіл ефективності 100 випадкових систем")
    ax.set_xlabel("Ефективність (%)")
    ax.set_ylabel("Кількість систем")
    ax.grid(True)
    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True, fill='both')
    tk.Button(frame, text="Закрити", command=frame.destroy).pack(pady=5)

# GUI

system_descriptions = {
        "Poster": "Poster — хмарна POS-система для ресторанів, барів та кафе з простим інтерфейсом і підтримкою мобільних пристроїв.",
        "Cashalot": "Cashalot — доступна POS-система для малих закладів, підтримує оффлайн-режим і основні облікові функції.",
        "Syrve": "Syrve — потужна система для великих ресторанів і мереж з широкими аналітичними можливостями.",
        "ULTRA Company": "ULTRA — універсальна система з гнучкими налаштуваннями, підтримкою доставки та оффлайн-режиму.",
        "R-Keeper": "R-Keeper — рішення для мережевих закладів з розширеним функціоналом, масштабоване й професійне."
}

def launch_gui():
    all_features = features
    types = {
        1: "Кав'ярня",
        2: "Кафе",
        3: "Ресторан",
        4: "Бар / Паб",
        5: "Takeout заклад"
    }

    root = tk.Tk()
    root.title("Інтелектуальний підбір ПЗ")
    root.geometry("700x800")

    tk.Label(root, text="🔍 Оберіть тип закладу", font=("Helvetica", 12, "bold")).pack(pady=5)
    zaklad_var = tk.IntVar(value=1)
    for i, name in types.items():
        tk.Radiobutton(root, text=name, variable=zaklad_var, value=i).pack(anchor='w')

    tk.Label(root, text="\nОберіть бажані функції", font=("Helvetica", 12, "bold")).pack(pady=10)
    feature_vars = []
    for feature in all_features:
        var = tk.BooleanVar()
        feature_vars.append(var)
        cb = tk.Checkbutton(root, text=feature, variable=var)
        cb.pack(anchor='w')

    def clear_all():
        zaklad_var.set(1)
        for var in feature_vars:
            var.set(False)

    def process_selection():
        selected_indices = [i for i, var in enumerate(feature_vars) if var.get()]
        if not selected_indices:
            messagebox.showwarning("Увага", "Оберіть хоча б одну функцію.")
            return

        required_features = [features[i] for i in selected_indices]
        matches = {}
        for system in df.columns:
            f = df[system]
            if all(f.iloc[i] == 1 for i in selected_indices):
                matches[system] = [features[i] for i, val in enumerate(f) if val == 1]

        if not matches:
            messagebox.showwarning("Не знайдено", "Жодна система не відповідає всім вимогам.")
            return

        win = tk.Toplevel(root)
        win.title("Результати підбору")
        text = tk.Text(win, wrap="word")
        text.insert(tk.END, f"Тип закладу: {types.get(zaklad_var.get(), '')}\n\n")
        for name, feats in matches.items():
            extra = [f for f in feats if f not in required_features]
            text.insert(tk.END, f"🔹 {name}\n")
            text.insert(tk.END, f"   📌 {system_descriptions.get(name, '—')}\n")
            text.insert(tk.END, f"   ✅ Включає: {', '.join(required_features)}\n")
            if extra:
                text.insert(tk.END, f"   ➕ Також підтримує: {', '.join(extra)}\n")
            text.insert(tk.END, "\n")
        text.pack(expand=True, fill='both')
        tk.Button(win, text="Закрити", command=win.destroy).pack(pady=5)

    def show_charts():
        for i in range(1, 4):
            weights = get_weights(i)
            eff = calculate_effectiveness(weights)
            plot_effectiveness_in_window(eff, f"Індекс ефективності (Сценарій {i})", root)

        random_df = generate_random_systems(100)
        weighted_random = random_df.mul(pd.Series(get_weights(1)), axis=0)
        random_eff = weighted_random.sum()
        plot_stress_distribution_in_window(random_eff, root)
        plot_heatmap_window(root)

    def generate_random_systems(n=50):
        random_data = {}
        for i in range(n):
            name = f"System_{i+1}"
            random_data[name] = [random.randint(0, 1) for _ in features]
        return pd.DataFrame(random_data, index=features)

    tk.Button(root, text="🔍 Підібрати систему", command=process_selection).pack(pady=10)
    tk.Button(root, text="📊 Показати графіки ефективності", command=show_charts).pack(pady=5)
    tk.Button(root, text="🧹 Очистити", command=clear_all).pack(pady=5)
    root.mainloop()

# Запуск GUI
launch_gui()
