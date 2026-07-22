# Amazon Product Analyzer & Short Video Script Generator

A fun side-project built to analyze Amazon product pages, extract market insights, and automatically generate engaging short-video scripts with text-to-speech audio previews.

> **Project Note**: This is a personal hobby project created for exploration and learning. There are plenty of areas for improvement! Feedback, ideas, and suggestions are always welcome.

---

## 💡 Key Features

- **Product Parsing**: Automatically extract product details from Amazon URLs, with a manual fallback mode for pasting page text/HTML directly.
- **Market Insights**: Leverage LLMs (Gemini) to deduce target audiences, typical usage scenarios, customer pain points, and core selling propositions.
- **Short Video Scripts**: Generate oral scripts tailored to various styles (enthusiastic, professional, storytelling, or humorous), formatted within 150 characters (Hook, Body, and Call-to-Action).
- **Audio Previews**: Integrated neural text-to-speech (Edge TTS) for streaming audio playback, multiple voice characters, and MP3 downloads.

---

## 🚀 Quick Start

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/Amazon_Product_Tool.git
cd Amazon_Product_Tool

# Create & activate a virtual environment
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate

# Install requirements
pip install -r requirements.txt
playwright install chromium
```

### 2. Environment Configuration

Copy `.env.example` to `.env` and set your Gemini API key:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### 3. Run the App

```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` in your browser to try it out!

---

## 💬 Community & Discussions

This project is open-ended and constantly evolving. If you run into issues or have ideas for improvement (e.g., supporting additional e-commerce sites, refining script generation prompts, or adding new voice features), feel free to connect:

- Open an **Issue** to report bugs or request features
- Start a thread in **Discussions** to share ideas
- Submit a **Pull Request** to help improve the project!

---

## 📄 License

Distributed under the [MIT License](LICENSE).
