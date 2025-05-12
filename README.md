# INFILTRE 🕵️‍♂️🔐

INFILTRE is a powerful Python tool for discovering exposed sensitive files and misconfigurations on web servers.  
It scans for publicly accessible secrets like API keys, database credentials, and configuration files.  
Developed by Cipher Squid — use it responsibly! ☠️

---

## ✨ Features

- 📂 **Smart fuzzing** of hidden paths and sensitive files
- 🔍 **Automatic detection** of secrets (API keys, tokens, DB creds, etc.)
- ⚡ **Multithreaded scanning** for high performance
- ⏱️ **Configurable delay and timeout**
- 🛡️ **Proxy support** and basic rate-limit handling
- 🧰 **Supports custom wordlists** and manual file input
- 📄 **Saves results automatically** with timestamped output
- 🐞 **Verbose/debug mode** for deeper insights

---

## ▶️ Demo

```bash
=====================================
[×] INFILTRE Tool by 𝘾𝙞𝙥𝙝𝙚𝙧 𝙎𝙦𝙪𝙞𝙙
[×] Use responsibly!
=====================================
$ python INFILTRE.py -u https://example.com -w wordlist.txt -t 20 --verbose
```

---

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ciphersquid666/INFILTRE.git
   cd INFILTRE
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Usage

Run the script:
```bash
python INFILTRE.py -u https://target.com -w wordlist.txt
```

**Available options:**

| Flag            | Description                                     |
|-----------------|-------------------------------------------------|
| -u, --url       | Base URL to scan (e.g. https://example.com)     |
| -w, --wordlist  | Wordlist file with paths (one per line)         |
| -t, --threads   | Number of threads (default: 10)                 |
| -d, --delay     | Delay between requests in seconds               |
| -o, --output    | Output file name (default: results.txt)         |
| -p, --proxy     | Proxy to use (e.g. http://127.0.0.1:8080)       |
| --timeout       | Request timeout (default: 5 seconds)            |
| --verbose       | Enable detailed debug output                    |

---

## 📤 Output

- **Terminal** – highlights accessible and sensitive files
- **File** – results saved to `results_<timestamp>.txt`

---

## 🧰 Requirements

- `requests`
- `termcolor`

Install all with:
```bash
pip install -r requirements.txt
```

---

## ⚠️ Disclaimer

This tool is intended for **educational and authorized testing purposes only**.  
Do not use it on websites or servers without proper permission.  
**Unauthorized use may be illegal and unethical.**

---

## 📜 License

Distributed under the **MIT License**.

---

## 👤 Author

**Cipher Squid**  
GitHub: [@ciphersquid666](https://github.com/ciphersquid666)
```

---

### **Suggerimenti finali**
- Inserisci tutto il testo tra triple backticks (\`\`\`) solo se vuoi mostrarlo come esempio di README; altrimenti, copia e incolla direttamente questo Markdown nel tuo README.md.
- Le tabelle renderizzano bene su GitHub e sono più chiare degli elenchi per le opzioni.
- Se vuoi aggiungere un banner o badge, puoi inserire il markdown per un’immagine (es: ![banner](url)) subito sotto il titolo.
