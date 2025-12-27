# 🛡️ ShadowReconX

## Advanced Modular Defensive Recon & Audit Tool (CLI + GUI)

**Educational • Blue Team • Internal Audit Only**

![ShadowReconX – Advanced Modular Defensive Recon & Audit Tool](https://github.com/mahdizebardastbarzin/ShadowReconX/blob/main/ShadowReconX.jpg)

---

## 📌 Project Overview | معرفی پروژه

**EN:**
ShadowReconX is a **modular defensive reconnaissance and system audit tool** designed for Blue Team operations, internal security audits, SOC analysis, and educational purposes. It provides both **CLI** and **GUI** interfaces, offering deep visibility into system state, processes, resources, and potential risks — without performing any exploitative action.

**FA:**
ShadowReconX یک ابزار **شناسایی و ممیزی دفاعی ماژولار** است که برای تیم آبی، ممیزی امنیت داخلی، تحلیل SOC و اهداف آموزشی طراحی شده است. این ابزار بدون انجام هیچ‌گونه اکسپلویت، دید جامعی از وضعیت سیستم، پردازش‌ها و منابع ارائه می‌دهد و دارای رابط **خط فرمان** و **گرافیکی** می‌باشد.

---

## ✨ Key Features | قابلیت‌های کلیدی

### 🔹 Core Capabilities

* Modular plugin-based architecture
* Safe system enumeration (no exploitation)
* CLI + Professional GUI interface
* JSON & Text report export
* Cross-platform (Windows / Linux)

### 🔹 System Recon Modules

* OS, Kernel & Architecture detection
* CPU (cores, usage)
* Memory usage
* Disk partitions & usage
* Network interfaces & IPs
* Active process enumeration

### 🔹 Advanced Process Control (GUI)

* Live process table
* Risk scoring engine (0–100)
* Highlighted suspicious processes
* Terminate / Kill Tree / Suspend / Resume
* Full audit logging

### 🔹 Process Deep Inspection

* Open file handles per process
* Network connections per process
* Interactive popup for long values

---

## 🧠 Architecture Overview | معماری ابزار

```
ShadowReconX
│
├── Plugin Engine
│   ├── System Info
│   ├── CPU Info
│   ├── Memory Info
│   ├── Disk Info
│   ├── Network Info
│   └── Processes
│
├── Execution Engine
│   └── Aggregates all plugins
│
├── Export Module
│   ├── JSON Report
│   └── Text Report
│
├── CLI Interface
│
└── GUI Interface (Tkinter)
    ├── Dashboard
    ├── Process Manager
    └── Process Details Viewer
```

---

## 🔌 Plugin System | سیستم پلاگین

**EN:**
Each reconnaissance module is implemented as an isolated plugin and registered dynamically. This allows easy extension without touching the core engine.

**FA:**
هر بخش شناسایی به‌صورت یک پلاگین مستقل پیاده‌سازی شده و به‌صورت داینامیک ثبت می‌شود. این معماری توسعه ابزار را بسیار ساده و امن می‌کند.

### Registered Plugins

* System Info
* CPU Info
* Memory Info
* Disk Info
* Network Info
* Processes

---

## ⚙️ Execution Modes | حالت‌های اجرا

### ▶️ CLI Mode (Default)

```
python shadowreconx.py
```

**Features:**

* Prints full system audit to terminal
* Automatically exports reports

---

### 🖥️ GUI Mode

```
python shadowreconx.py --gui
```

**GUI Features:**

* Sidebar module navigation
* Dark professional theme
* Interactive process control
* Real-time refresh

---

## 📤 Report Export | خروجی گزارش‌ها

| Format    | File                     |
| --------- | ------------------------ |
| JSON      | shadowreconx_report.json |
| Text      | shadowreconx_report.txt  |
| Audit Log | shadowreconx_audit.log   |

Reports include timestamps, module data, and action logs.

---

## ⚠️ Risk Scoring Engine | موتور امتیازدهی ریسک

**EN:**
Processes are evaluated based on name patterns, privilege level, CPU usage, and abnormal states.

**FA:**
پردازش‌ها بر اساس نام مشکوک، سطح دسترسی، مصرف CPU و وضعیت غیرعادی امتیازدهی می‌شوند.

**Score Range:** `0 → 100`

* 0–39 → Low Risk
* 40–69 → Medium Risk
* 70–100 → High Risk

---

## 🔐 Security Design Principles | اصول امنیتی

* No exploitation
* No brute-force
* No persistence
* No network attacks
* Local audit only

Designed strictly for **defensive security**.

---

## 🧑‍💻 Author

**Engineer:** Mahdi Zebardast Barzin
**GitHub:** [https://github.com/mahdizebardastbarzin](https://github.com/mahdizebardastbarzin)

---

## 📜 License

MIT License – Educational & Defensive Use Only

---

## 🚨 Security Warning | هشدار امنیتی

**EN:**
Using this tool on systems you do not own or have permission for is illegal.

**FA:**
استفاده از این ابزار روی سیستم‌هایی که مالک آن نیستید یا مجوز ندارید، غیرقانونی است.

---

## 🛣️ Roadmap | نقشه راه

* Plugin sandboxing
* Encrypted reports
* SOC dashboard
* YARA rule integration
* Windows service inspection

---

**ShadowReconX — Visibility without exploitation.**


