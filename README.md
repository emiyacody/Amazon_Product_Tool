# Amazon 智能商品分析与短视频口播生成工具 (Amazon Product Analyzer & Script Generator)

这是一个现代化、全栈设计的 Amazon 商品分析与视频口播文案生成系统。输入任意亚马逊商品链接或粘贴页面内容，系统将自动提取商品关键信息，利用 Gemini 大模型进行多维度深度市场分析（包括目标人群、痛点分析、核心卖点等），并智能生成符合 150 字以内限制的短视频口播脚本，同时集成微软 Edge 神经网络 TTS（语音合成），支持多种方言与男女声的在线朗读和音频下载。

---

## 🌟 核心功能

1. **🚀 智能双输入模式**
   - **自动抓取**：采用 Playwright 无头浏览器技术，模拟真实用户请求，绕过基本的反爬机制，自动解析亚马逊商品详情页。
   - **手动粘贴 (备用)**：如果自动抓取因反爬锁区或网络问题受阻，支持直接粘贴网页 HTML 源码或关键文本，同样能完成高精度解析。

2. **🧠 Gemini 深度市场研判 (JSON Schema 强约束)**
   - 使用 Google Gemini API 进行一次性高效率分析，提取目标受众群体、真实使用场景、用户痛点、核心差异化卖点。
   - 使用 Pydantic 的 `ProductAnalysisSchema` 实施结构化 JSON 输出控制，确保大模型响应格式 100% 稳定，免去解析出错的烦恼。

3. **✍️ 4 种风格的短视频口播文案生成**
   - **激情带货风**：热情高亢，多用感叹号，富有煽动性，强调限时抢购（“家人们冲它！”）。
   - **专业客观风**：侧重技术参数、材质工艺和真实对比，以理服人。
   - **生活种草风**：闺蜜日常分享口吻，从具体生活尴尬或烦恼场景切入，平实自然。
   - **幽默搞笑风**：风趣吐槽，放大痛点尴尬，将产品作为搞笑反转后的救星引出。
   - **150字严控**：所有风格口播均严格控制在 150 字内，分为“黄金5秒钩子 (Hook)”、“核心内容 (Body)”与“行动呼吁 (CTA)”三段式，并提供一键复制。

4. **🎙️ 微软 Edge 神经网络 TTS 实时配音**
   - 集成 `edge-tts` 库，支持流式传输音频，响应极快，无需等待整段音频合成完毕即可开始播放。
   - 提供多种高品质配音角色：晓晓（温柔女声）、云希（活力带货男声）、云健（稳重科普男声），以及**东北大妹子**和**陕西秦腔女声**等方言特色配音，极大增强短视频的趣味性与本土化吸引力。
   - 支持一键试听和合成音频文件下载。

5. **⚡ 双重本地缓存设计 (Sub-50ms 响应)**
   - 对抓取的数据及 Gemini 分析结果进行本地 MD5 哈希命名缓存，完全杜绝重复抓取和 API 调用。
   - 相同产品及相同风格再次查询时，API 响应时间从数秒直接降至 **50 毫秒以内**，大幅节约 API Token 消耗并提升用户体验。

6. **🎨 极具视觉冲击力的毛玻璃暗黑风 UI**
   - 精心定制的 HSL 渐变光晕背景与深色毛玻璃卡片（Glassmorphism）。
   - 细致的悬停微动画与流式加载状态骨架，带来极佳的感官体验。

---

## 🛠️ 技术栈

### 后端 (Backend)
- **FastAPI**: 异步高性能 Web 框架。
- **Playwright**: 自动化浏览器，用于抓取复杂的 Amazon 商品详情页。
- **BeautifulSoup4**: HTML 解析与关键标签数据清洗。
- **google-generativeai**: Google Gemini 官方 SDK。
- **Pydantic v2**: 强类型数据验证与 JSON 结构约束。
- **edge-tts**: 微软 Edge 神经网络语音合成流式接口。
- **python-dotenv**: 环境配置文件管理。

### 前端 (Frontend)
- **HTML5 & CSS3**: 现代化 Vanilla CSS 架构，响应式栅格布局（CSS Grid & Flexbox）。
- **JavaScript (ES6+)**: 原生异步请求（Fetch API）、音频上下文流式播放控制及动态 DOM 渲染。
- **FontAwesome & Google Fonts**: 精美图标库与 Outfit/Inter 现代字体家族。

---

## 📂 项目结构

```text
product-analyze-tool/
├── app/
│   ├── __init__.py
│   ├── analyzer.py       # Gemini API 分析器与 Schema 约束定义
│   ├── main.py           # FastAPI 服务入口及缓存管理、TTS 端点
│   ├── schemas.py        # Pydantic 响应结构体声明
│   └── scraper.py        # Playwright & BeautifulSoup4 商品解析器
├── static/
│   ├── app.js            # 前端交互与音频流式播放逻辑
│   ├── index.html        # 前端 UI 主页面
│   └── style.css         # 现代化暗黑毛玻璃样式表
├── cache/                # 本地缓存目录（自动生成，已在 gitignore 中忽略）
├── verify_gemini.py      # Gemini API 连通性测试脚本
├── verify_scraper.py     # Playwright 网页抓取功能测试脚本
├── verify_analyzer.py    # 离线大模型分析及 150字规格校验脚本
├── verify_api.py         # FastAPI 路由及本地缓存命中校验脚本
├── mock_product.json     # 本地测试用的商品数据样例
├── requirements.txt      # 后端依赖包清单
├── .env.example          # 环境配置模板
└── README.md             # 项目说明文档
```

---

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/product-analyze-tool.git
cd product-analyze-tool
```

### 2. 创建并激活虚拟环境
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖项
```bash
pip install -r requirements.txt
```

### 4. 安装 Playwright 浏览器内核
Playwright 抓取器需要安装 Chromium 浏览器内核：
```bash
playwright install chromium
```

### 5. 配置环境变量
复制 `.env.example` 并重命名为 `.env`：
```bash
# Windows cmd
copy .env.example .env

# Windows PowerShell 或 Linux/macOS
cp .env.example .env
```
用文本编辑器打开 `.env` 并填写您的 Gemini API Key：
```env
GEMINI_API_KEY=YOUR_ACTUAL_GEMINI_API_KEY
GEMINI_MODEL=gemini-3.5-flash
```

---

## 🧪 功能验证

项目自带了 4 个独立的校验脚本，方便您在部署或二次开发时快速验证核心链路是否正常运行：

1. **验证 Gemini 连通性**：
   ```bash
   python verify_gemini.py
   ```
2. **验证网页抓取**（传入任意 Amazon 商品链接）：
   ```bash
   python verify_scraper.py https://www.amazon.com/dp/B07FZ8S74R
   ```
3. **验证大模型分析与 150 字文案硬指标规范**（基于 verify_scraper 生成的本地 mock 数据，无需连网重新抓取）：
   ```bash
   python verify_analyzer.py
   ```
4. **验证后端 API 与本地双重缓存命中速度**：
   ```bash
   python verify_api.py
   ```

---

## 💻 启动运行

启动 FastAPI 服务：
```bash
uvicorn app.main:app --reload
```

启动成功后，在浏览器中访问：
[**`http://127.0.0.1:8000`**](http://127.0.0.1:8000) 即可使用完整的图形化操作台。

---

## ⚠️ 注意事项

- **反爬保护**：部分 Amazon 商品页会触发验证码或阻断行为，如果自动抓取失败，请在控制台一键切换到 **“网页内容粘贴模式”**，手动将商品页的文本/HTML 粘贴至输入框。
- **API 额度安全**：请绝对不要将包含真实密钥的 `.env` 文件提交到 GitHub。项目自带的 `.gitignore` 已将 `.env` 排除。
- **TTS 连网要求**：`edge-tts` 需要向微软 Edge TTS 服务器建立 WebSocket 连接，请确保运行环境的网络可顺畅访问外网。

---

## 📝 许可证

本项目采用 [MIT License](LICENSE) 许可协议。
