import tkinter as tk
import random
import threading
import winsound
import time

# ================= НАСТРОЙКИ =================
PASSWORD = "987654321"
MAX_ATTEMPTS = 3
TIME_LIMIT = 60

attempts_left = MAX_ATTEMPTS
time_left = TIME_LIMIT
blocked = False

# ================= ASCII АНІМАЦІЯ =================
FRAMES = [
"""
        . . . . .
      . . . . . . .
    . . . . . . . . .
      . . . . . . .
        . . . . .
""",
"""
      . . . . . . .
    . . . . . . . . .
  . . . . . . . . . . .
    . . . . . . . . .
      . . . . . . .
""",
"""
    . . . . . . . . .
  . . . . . . . . . . .
. . . . . . . . . . . . .
  . . . . . . . . . . .
    . . . . . . . . .
"""
]

frame_index = 0
blink = True

# ================= АВАРІЙНИЙ ВИХІД =================
def emergency_exit(e):
    if e.keysym in ("Insert", "Delete", "End"):
        root.destroy()

def key_blocker(e):
    # дозволяємо тільки Enter + аварійні клавіші
    if e.keysym in ("Return", "Insert", "Delete", "End"):
        return
    return "break"

# ================= МУЗИКА =================
def play_music():
    while not blocked:
        winsound.Beep(200, 150)  # короткий і тихіший звук
        winsound.Beep(150, 100)  # короткий і тихіший звук

# ================= АНІМАЦІЇ =================
def animate():
    global frame_index
    art_label.config(text=FRAMES[frame_index])
    frame_index = (frame_index + 1) % len(FRAMES)
    root.after(600, animate)

def blink_title():
    global blink
    title.config(fg="red" if blink else "black")
    blink = not blink
    root.after(500, blink_title)

def glitch(widget):
    x = random.randint(-5, 5)
    y = random.randint(-5, 5)
    widget.place_configure(x=x, y=y)
    root.after(100, lambda: widget.place_configure(x=0, y=0))

# ================= СПРОБИ =================
def update_attempt_dots():
    dots = "● " * attempts_left + "○ " * (MAX_ATTEMPTS - attempts_left)
    attempt_dots.config(text=dots.strip())

def show_attempt_popup():
    popup = tk.Toplevel(root)
    popup.attributes("-fullscreen", True)
    popup.configure(bg="black")

    label = tk.Label(
        popup,
        text=f"ЗАЛИШИЛОСЬ {attempts_left} СПРОБ",
        fg="red",
        bg="black",
        font=("Arial", 48, "bold")
    )
    label.pack(expand=True)

    alpha = 1.0
    def fade():
        nonlocal alpha
        alpha -= 0.05
        if alpha <= 0:
            popup.destroy()
        else:
            popup.attributes("-alpha", alpha)
            popup.after(80, fade)
    fade()

# ================= ЧЕРВОНІ ПОПЕРЕДЖЕННЯ =================
warnings_text = [
    "⚠ НЕСАНКЦІОНОВАНИЙ ДОСТУП",
    "⚠ ФАЙЛИ ШИФРУЮТЬСЯ",
    "⚠ СИСТЕМА ЗАБЛОКОВАНА",
    "⚠ ВТРАТА ДАНИХ"
]

def flashing_warning():
    if blocked:
        return

    label = tk.Label(
        root,
        text=random.choice(warnings_text),
        fg="red",
        bg="black",
        font=("Arial", 26, "bold")
    )

    x = random.randint(50, root.winfo_screenwidth() - 600)
    y = random.randint(50, root.winfo_screenheight() - 100)
    label.place(x=x, y=y)

    root.after(700, label.destroy)
    root.after(900, flashing_warning)

# ================= ФЕЙКОВЕ ШИФРУВАННЯ =================
def fake_encryption():
    popup = tk.Toplevel(root)
    popup.attributes("-fullscreen", True)
    popup.configure(bg="black")

    label = tk.Label(
        popup,
        text="ШИФРУВАННЯ ФАЙЛІВ: 0%",
        fg="red",
        bg="black",
        font=("Arial", 42, "bold")
    )
    label.pack(expand=True)

    percent = 0

    def update():
        nonlocal percent
        if percent < 100:
            percent += random.randint(1, 5)
            label.config(text=f"ШИФРУВАННЯ ФАЙЛІВ: {min(percent,100)}%")
            popup.after(400, update)
        else:
            label.config(text="ВСІ ФАЙЛИ ЗАШИФРОВАНІ")

    update()

# ================= ЛОГІКА =================
def unlock(event=None):
    global attempts_left

    if blocked:
        return

    if entry.get() == PASSWORD:
        root.destroy()
    else:
        attempts_left -= 1
        entry.delete(0, tk.END)
        update_attempt_dots()
        glitch(main_frame)

        if attempts_left > 0:
            show_attempt_popup()
        else:
            block_access()

def block_access():
    global blocked
    blocked = True
    entry.config(state="disabled")
    unlock_button.config(state="disabled")
    timer_label.config(text="ДОСТУП ЗАБЛОКОВАНО")
    fake_encryption()

def countdown():
    global time_left

    if time_left > 0 and not blocked:
        timer_label.config(text=f"ЗАЛИШИЛОСЬ ЧАСУ: {time_left} СЕК")
        time_left -= 1
        root.after(1000, countdown)
    elif not blocked:
        block_access()

# ================= ROOT =================
root = tk.Tk()
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)
root.configure(bg="black")
root.protocol("WM_DELETE_WINDOW", lambda: None)

# 🔒 БЛОК КЛАВІШ + АВАРІЙНИЙ ВИХІД
root.bind_all("<Key>", key_blocker)
root.bind("<Return>", unlock)
root.bind("<Insert>", emergency_exit)
root.bind("<Delete>", emergency_exit)
root.bind("<End>", emergency_exit)

main_frame = tk.Frame(root, bg="black")
main_frame.place(relx=0.5, rely=0.5, anchor="center")

art_label = tk.Label(main_frame, fg="red", bg="black", font=("Consolas", 30))
art_label.pack()

title = tk.Label(
    main_frame,
    text="ДОСТУП ЗАБОРОНЕНО",
    fg="red",
    bg="black",
    font=("Arial", 36, "bold")
)
title.pack(pady=20)

attempt_dots = tk.Label(main_frame, fg="red", bg="black", font=("Arial", 20))
attempt_dots.pack()
update_attempt_dots()

entry = tk.Entry(main_frame, show="*", font=("Arial", 26), justify="center", width=20)
entry.pack(pady=15)
entry.focus_set()

unlock_button = tk.Button(
    main_frame,
    text="РОЗБЛОКУВАТИ",
    command=unlock,
    font=("Arial", 20),
    width=18
)
unlock_button.pack(pady=10)

timer_label = tk.Label(main_frame, fg="yellow", bg="black", font=("Arial", 18))
timer_label.pack()

# ================= ЗАПУСК =================
threading.Thread(target=play_music, daemon=True).start()
animate()
blink_title()
countdown()
root.after(2000, flashing_warning)

root.mainloop()
