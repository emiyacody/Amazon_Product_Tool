# Amazon 商品分析与短视频文案生成器

这是一个出于个人兴趣开发的辅助小工具，主要用于帮助自己和有需要的朋友快速分析亚马逊商品信息，并自动生成适合短视频播报的口播文案与配音试听。

> **项目说明**：本项目纯属个人探索与兴趣实践，代码和功能尚有许多可以优化和完善的地方。非常欢迎有兴趣的朋友体验、提出建议，或者一起探讨交流！

---

## 💡 主要功能

- **商品信息解析**：支持输入亚马逊商品链接自动提取页面信息，同时也支持手动粘贴页面文本作为备用模式。
- **深度市场洞察**：利用大模型分析商品的目标受众、典型使用场景、用户痛点与核心卖点。
- **短视频口播生成**：提供激情带货、专业客观、生活种草、幽默吐槽等多种文案风格，控制在 150 字以内的短视频口播结构（包含黄金 5 秒钩子、主体内容与 Call to Action）。
- **语音在线试听**：支持语音合成与流式朗读，提供多种配音角色与特色方言试听及音频下载。

---

## 🚀 快速开始

### 1. 克隆项目与安装依赖

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/Amazon_Product_Tool.git
cd Amazon_Product_Tool

# 创建并激活虚拟环境
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
playwright install chromium
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并填写你的 Gemini API 密钥：

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### 3. 启动服务

```bash
uvicorn app.main:app --reload
```

启动后在浏览器访问 `http://127.0.0.1:8000` 即可体验。

---

## 💬 交流与讨论

这个项目目前还处于个人折腾阶段，如果你在体验过程中遇到了问题，或者有任何好的想法（比如支持更多的抓取渠道、优化文案生成 prompt、增加新的配音风格等），非常欢迎交流：

- 提交 **Issues** 提出问题或功能建议
- 参与 **Discussions** 探讨有趣的玩法与后续规划
- 欢迎提交 **PR** 一起完善代码！

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 许可协议。
