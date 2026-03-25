import tkinter as tk
from tkinter import ttk
import time
import math
import re
import hashlib
import requests

# -----------------------------
# ASCII BANNER
# -----------------------------
BANNER = r"""
███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗
██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║
███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║
╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║
███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝

 ██████╗██████╗ ██╗   ██╗██████╗ ████████╗
██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝
██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   
██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   
╚██████╗██║  ██║   ██║   ██║        ██║   
 ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝   
  
                             ShadowCrypt X Analyzer
                                  Built By Amal
"""

# -----------------------------
# PASSWORD ANALYSIS
# -----------------------------
common_patterns = ["12345","password","qwerty","admin","Password@123","admin123","root","root123",
"user","user123","login","login123","welcome","welcome123","abc123","test","test123","guest",
"guest123","letmein","letmein123","monkey","dragon","football","iloveyou","shadow","shadow123",
"master","master123","hello","hello123","freedom","freedom123","whatever","trustno1",
"sunshine","princess","charlie","donald","superman","batman","zaq1zaq1","qazwsx",
"123","1234","123456","111","000","999","987654","1q2w3e4r","pass","admin@123",
"india","kerala","amal","shadowcrypt","god","king","queen","secret","default"]

def calculate_entropy(password):
    pool = 0
    if re.search(r"[a-z]", password): pool += 26
    if re.search(r"[A-Z]", password): pool += 26
    if re.search(r"[0-9]", password): pool += 10
    if re.search(r"[!@#$%^&*()_+=-]", password): pool += 20
    if pool == 0:
        return 0
    return round(len(password) * math.log2(pool), 2)

def estimate_crack_time(entropy):
    guesses_per_sec = 1e10
    seconds = (2 ** entropy) / guesses_per_sec

    if seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds/60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds/3600)} hours"
    elif seconds < 31536000:
        return f"{int(seconds/86400)} days"
    else:
        return f"{int(seconds/31536000)} years"

def analyze_password(password):
    entropy = calculate_entropy(password)
    suggestions = []
    patterns_found = []

    for p in common_patterns:
        if p in password.lower():
            patterns_found.append(p)

    if len(password) < 8:
        suggestions.append("Use at least 8 characters")
    if not re.search(r"[A-Z]", password):
        suggestions.append("Add uppercase letters")
    if not re.search(r"[0-9]", password):
        suggestions.append("Add numbers")
    if not re.search(r"[!@#$%^&*()_+=-]", password):
        suggestions.append("Add special characters")

    if entropy < 40:
        strength = "Weak"
    elif entropy < 60:
        strength = "Medium"
    else:
        strength = "Strong"

    return strength, entropy, suggestions, patterns_found

# -----------------------------
# HIBP CHECK
# -----------------------------
def check_pwned(password):
    try:
        sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
        prefix = sha1[:5]
        suffix = sha1[5:]
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return "API Error"

        for line in response.text.splitlines():
            h_suffix, count = line.split(":")
            if h_suffix == suffix:
                return int(count)

        return 0
    except:
        return "Error"

# -----------------------------
# GUI SETUP
# -----------------------------
root = tk.Tk()
root.title("ShadowCrypt Analyzer")
root.configure(bg="black")
root.geometry("900x650")

output = tk.Text(root, bg="black", fg="#00ff00",
                 font=("Courier", 14, "bold"),
                 borderwidth=0, insertbackground="white")
output.pack(fill="both", expand=True)

scrollbar = tk.Scrollbar(root, command=output.yview)
scrollbar.pack(side="right", fill="y")
output.config(yscrollcommand=scrollbar.set)

progress = ttk.Progressbar(root, orient="horizontal",
                           length=400, mode="determinate")
progress.pack(pady=5)

output.tag_config("green", foreground="#00ff00")
output.tag_config("red", foreground="#ff0033")
output.tag_config("yellow", foreground="#ffff00")

entry_frame = tk.Frame(root, bg="black")
entry_frame.pack(pady=10)

entry = tk.Entry(entry_frame, width=40, font=("Courier", 14))
entry.pack(side="left", padx=10)

btn = tk.Button(entry_frame, text="Analyze", command=lambda: run_analysis(),
                bg="black", fg="#00ff00")
btn.pack(side="left")

# -----------------------------
# TYPE EFFECT
# -----------------------------
def type_text(text, tag="green", delay=0.0008):
    for char in text:
        output.insert(tk.END, char, tag)
        output.see(tk.END)
        output.update()
        time.sleep(delay)

def show_banner():
    output.delete(1.0, tk.END)
    type_text(BANNER)

# -----------------------------
# MAIN LOGIC (UPDATED)
# -----------------------------
def run_analysis():
    password = entry.get()
    masked = "*" * len(password)

    output.insert(tk.END, "\n[+] Analyzing Password...\n", "yellow")
    output.insert(tk.END, f"[+] Input Password: {masked}\n")

    strength, entropy, suggestions, patterns = analyze_password(password)
    pwned = check_pwned(password)
    crack_time = estimate_crack_time(entropy)

    # ✅ NEW LOGIC: If breached → force Weak
    if isinstance(pwned, int) and pwned > 0:
        strength = "Weak"

    progress['value'] = min(entropy, 100)

    color = "green"
    if strength == "Weak":
        color = "red"
    elif strength == "Medium":
        color = "yellow"

    output.insert(tk.END, f"[+] Strength: {strength}\n", color)
    output.insert(tk.END, f"[+] Entropy: {entropy}\n")
    output.insert(tk.END, f"[+] Crack Time: {crack_time}\n")

    if patterns:
        output.insert(tk.END, f"[!] Patterns: {patterns}\n", "red")

    if isinstance(pwned, int):
        if pwned > 0:
            output.insert(tk.END, f"[!] BREACHED {pwned} TIMES ⚠️\n", "red")
        else:
            output.insert(tk.END, "[+] Not found in breaches ✅\n", "green")
    else:
        output.insert(tk.END, "[!] Pwned check failed\n", "yellow")

    if suggestions:
        output.insert(tk.END, "[!] Suggestions:\n", "yellow")
        for s in suggestions:
            output.insert(tk.END, f"   - {s}\n", "yellow")

    output.insert(tk.END, "\n")
    output.see(tk.END)

# -----------------------------
# START
# -----------------------------
root.after(100, show_banner)
root.mainloop()
