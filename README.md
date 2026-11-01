# Copify

**Copify** is a lightweight, zero-configuration Python utility that lets you seamlessly share your clipboard history with other devices over your Local Area Network (LAN). Built purely in Python with standard libraries, it requires no complex installations—just run the script, copy text on one machine, and access it on another.

## 🚀 Key Features

*   **LAN Clipboard Sharing:** Access your clipboard history from any device connected to the same local network.
*   **Simple History Management:** Effortlessly copy text from the history or clear the entire history list with a single click.
*   **Zero Dependencies:** Runs entirely on Python's built-in libraries (`tkinter`, `http.server`, `socket`). No `pip install` required.
*   **Single-File Execution:** Easy to deploy—just download the single `copify.py` script and run it.

## 📦 Requirements

*   **Python 3.x**
*   Works across Windows, macOS, and Linux (ensure `tkinter` is installed on Linux via `sudo apt-get install python3-tk`).

## 🛠️ Getting Started

### 1. Run the Application
Download `copify.py` to your machine, open your terminal or command prompt, and run:

```bash
python3 copify.py
```

### 2. Accessing the Clipboard
*   **Locally:** The graphical user interface (GUI) will open immediately on your machine, allowing you to manage your history and copy items.
*   **Across the LAN:** The terminal will display a local network URL (e.g., `http://192.168.1.5:8080`). Open this link in the web browser of any device on the same Wi-Fi or local network to view and grab your clipboard history!

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to contribute.

## 📜 License

This project is licensed under the MIT License.
