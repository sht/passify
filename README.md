# Passify

A beautiful, lightweight, and customisable password generator web app.  
Built with Flask, Bootstrap, and Docker. No database required.

## Demo

- [passify.sek4.com](https://passify.sek4.com/)

<img width="1344" height="609" alt="image" src="https://github.com/user-attachments/assets/86e56d3e-0cce-4bd3-a5ae-27930a899d5e" />


## ✨ Features

- Generate strong random passwords
- Set password length and minimum counts for uppercase, lowercase, and numbers
- Optionally include special characters
- View the last 100 generated passwords with UTC timestamps
- Clean, responsive Bootstrap UI
- No database—just a simple `history.txt` file
- Docker-ready for easy deployment

## 🚀 Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/passify.git
cd passify
```

### 2. Build and run with Docker

```bash
docker build -t passify .
docker run -p 5000:5000 -v \$(pwd)/history.txt:/app/history.txt passify
```

### 3. Open in your browser

Go to [http://localhost:5000](http://localhost:5000)

## 🖥️ Local Development

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## 🤝 Contributing

Contributions are welcome!  
- Fork the repo
- Create a feature branch
- Submit a pull request

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📢 Spread the Word

- Star this repo ⭐
- Share on social media
- Blog about it
- Submit issues and feature requests

## 📄 License

MIT License
