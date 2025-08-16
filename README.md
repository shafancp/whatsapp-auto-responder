# 🤖 WhatsApp Web Auto-Responder Bot  

A Python-based automation bot that integrates with **WhatsApp Web** using **Selenium**.  
The bot continuously monitors a group chat for a **trigger phrase** and automatically replies with predefined details (e.g., name and staff number).  

This project demonstrates skills in **web automation, real-time monitoring, and Selenium-based browser control**.  

---

## 🔑 Key Features
- **Real-time Monitoring** → Listens to new messages in a selected WhatsApp group.  
- **Trigger Detection** → Responds only when a specific phrase (e.g., `"your name and staff number"`) is found.  
- **Automated Response** → Sends your details instantly, only once per day to prevent spam.  
- **Persistent Session** → Saves Chrome user data locally, so you don’t need to scan the QR code every time.  
- **Error Handling** → Built-in recovery from stale elements and page reloads.  

---

## 🛠️ Technologies Used
- Python **3.8+**  
- **Selenium WebDriver** for browser automation  
- **WebDriver Manager** for ChromeDriver handling  
- **WhatsApp Web** as the target platform  

---

## ⚙️ Installation & Setup  

### 1. Clone Repository
git clone https://github.com/your-username/whatsapp-auto-bot.git
cd whatsapp-auto-bot

### 2. Install Dependencies
pip install selenium webdriver-manager

### 3. Configure Your Details
**Edit main.py and set your personal values:**
FULL_NAME = "Your Name"
STAFF_NUMBER = "00000"
GROUP_NAME = "Group Name
TRIGGER_PHRASE = "Trigger Message"

### 4. Run the Script
python main.py
On the first run, scan the WhatsApp QR code.

A User_Data folder will be created to store your Chrome session.
Future runs will automatically log you in without scanning.

