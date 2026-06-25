# 🕉️ Hindu Panchang AI Video Generator

Sirf **ek command** se roz ka panchang + video content ready!

```
python main.py
```

---

## 📁 Project Structure

```
panchang_project/
│
├── main.py              ← 👈 SIRF YAHI CHALAO!
│
├── config/
│   └── settings.py      ← Apni settings yahan badlein
│
├── core/
│   ├── panchang.py      ← Panchang calculate karta hai
│   ├── script_generator.py ← Video script banata hai
│   ├── video_prompts.py ← AI sites ke liye prompts
│   ├── saver.py         ← Files save karta hai
│   └── logger.py        ← Logs likhta hai
│
├── output/              ← Yahan files save hongi (auto-create)
└── logs/                ← Run history (auto-create)
```

---

## 🚀 Commands

```bash
# Aaj ka panchang (most common)
python main.py

# Kisi specific date ka
python main.py --date 2026-07-15

# Roz subah 5 baje automatic
python main.py --scheduler

# Setup check karo
python main.py --check
```

---

## ⚙️ Settings (config/settings.py)

Apna shehar, timing, channel name badlein:

```python
CITY           = "Kota"           # Apna shehar
DAILY_RUN_TIME = "05:00"          # Subah 5 baje
CHANNEL_NAME   = "Aaj Ka Panchang"
ANTHROPIC_API_KEY = "sk-ant-..."  # Optional - better scripts
```

---

## 🎬 Free AI Video Sites

Output HTML mein "Copy Prompt" button dabao aur paste karo:

| Site | Link | Kya milega |
|------|------|------------|
| InVideo | https://invideo.io | Best Hindi videos |
| Fliki | https://app.fliki.ai | Text to video + voice |
| Canva | https://canva.com/video | Templates |
| D-ID | https://d-id.com | AI avatar pandit |
| Pictory | https://pictory.ai | Script to video |

---

🙏 Jai Shri Ram!
