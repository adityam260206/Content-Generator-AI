# AI Content Generator 🤖

A modern, AI-powered content generation web application built with Next.js and powered by Google Gemini AI. Generate high-quality content for blogs, social media, emails, product descriptions, and more with real-time streaming responses.

![AI Content Generator](https://img.shields.io/badge/Next.js-16-black?style=flat-square&logo=next.js)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?style=flat-square&logo=typescript)
![Gemini AI](https://img.shields.io/badge/Gemini-AI-blue?style=flat-square&logo=google)

## ✨ Features

- **Real-time Streaming**: Watch your content generate in real-time with streaming responses
- **Multiple Content Types**: 
  - Blog posts and articles
  - Social media posts
  - Professional emails
  - Product descriptions
  - Creative writing
  - Content summaries
- **Customizable Tone**: Choose from professional, casual, friendly, formal, humorous, or persuasive tones
- **Modern UI**: Beautiful gradient design with glassmorphism effects
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Copy to Clipboard**: Easily copy generated content with one click

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ installed
- A Google Gemini API key (get one at [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/adityam260206/content-generator-AI.git
cd content-generator-AI
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env.local
```

4. Add your Gemini API key to `.env.local`:
```
GEMINI_API_KEY=your_actual_api_key_here
```

5. Run the development server:
```bash
npm run dev
```

6. Open [http://localhost:3000](http://localhost:3000) in your browser

## 🛠️ Tech Stack

- **Framework**: Next.js 16 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **AI Model**: Google Gemini Pro
- **Deployment**: Vercel (recommended)

## 📖 Usage

1. **Select Content Type**: Choose what type of content you want to generate (blog post, social media, etc.)
2. **Choose Tone**: Pick the tone that matches your needs (professional, casual, etc.)
3. **Enter Your Prompt**: Describe what you want the AI to create
4. **Generate**: Click the generate button and watch the AI create your content in real-time
5. **Copy & Use**: Copy the generated content and use it wherever you need

## 🎨 Screenshots

### Main Interface
The app features a beautiful gradient design with real-time content generation:
- Left panel: Input configuration
- Right panel: Live streaming output
- Bottom: Feature highlights

## 🔒 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Your Google Gemini API key | Yes |

## 🚢 Deployment

### Deploy to Vercel

The easiest way to deploy this app is using Vercel:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/adityam260206/content-generator-AI)

1. Click the button above
2. Add your `GEMINI_API_KEY` environment variable
3. Deploy!

### Manual Deployment

1. Build the project:
```bash
npm run build
```

2. Start the production server:
```bash
npm start
```

## 📝 API Route

The app includes a streaming API endpoint at `/api/generate`:

```typescript
POST /api/generate
Content-Type: application/json

{
  "prompt": "Write a blog post about AI",
  "contentType": "blog",
  "tone": "professional"
}
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Aditya M**
- GitHub: [@adityam260206](https://github.com/adityam260206)

## 🙏 Acknowledgments

- Built with [Next.js](https://nextjs.org/)
- Powered by [Google Gemini AI](https://ai.google.dev/)
- Styled with [Tailwind CSS](https://tailwindcss.com/)

---

⭐ Star this repo if you find it helpful!
