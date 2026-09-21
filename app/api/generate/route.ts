import { GoogleGenerativeAI } from '@google/generative-ai';
import { NextRequest } from 'next/server';

// Initialize the Gemini client
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY || '');

export async function POST(req: NextRequest) {
  try {
    const { prompt, contentType, tone } = await req.json();

    if (!prompt) {
      return new Response('Prompt is required', { status: 400 });
    }

    if (!process.env.GEMINI_API_KEY) {
      return new Response('API key not configured', { status: 500 });
    }

    // Build the system prompt based on content type and tone
    const systemPrompt = buildSystemPrompt(contentType, tone);

    // Combine system prompt with user prompt
    const fullPrompt = `${systemPrompt}\n\nUser Request: ${prompt}`;

    // Get the generative model
    const model = genAI.getGenerativeModel({ model: 'gemini-pro' });

    // Generate content with streaming
    const result = await model.generateContentStream(fullPrompt);

    // Create a ReadableStream to pipe the response
    const readableStream = new ReadableStream({
      async start(controller) {
        try {
          for await (const chunk of result.stream) {
            const text = chunk.text();
            controller.enqueue(new TextEncoder().encode(text));
          }
          controller.close();
        } catch (error) {
          controller.error(error);
        }
      },
    });

    return new Response(readableStream, {
      headers: {
        'Content-Type': 'text/plain; charset=utf-8',
        'Transfer-Encoding': 'chunked',
      },
    });
  } catch (error) {
    console.error('Error generating content:', error);
    return new Response('Error generating content', { status: 500 });
  }
}

function buildSystemPrompt(contentType: string, tone: string): string {
  const toneDescriptions: Record<string, string> = {
    professional: 'professional and polished',
    casual: 'casual and conversational',
    friendly: 'warm and friendly',
    formal: 'formal and academic',
    humorous: 'light-hearted and humorous',
    persuasive: 'persuasive and compelling',
  };

  const contentTypeInstructions: Record<string, string> = {
    blog: 'Write a well-structured blog post with an engaging introduction, informative body paragraphs, and a strong conclusion. Include relevant headings where appropriate.',
    social: 'Write a concise and engaging social media post that captures attention quickly. Keep it short and impactful, suitable for platforms like Twitter, LinkedIn, or Instagram.',
    email: 'Write a professional email with a clear subject line, greeting, body, and closing. Structure the content for easy readability.',
    product: 'Write a compelling product description that highlights key features, benefits, and value propositions. Focus on persuading the reader.',
    creative: 'Write creative, imaginative content. Be expressive and engaging while maintaining coherence and quality.',
    summary: 'Provide a clear and concise summary that captures the main points. Be direct and informative.',
  };

  const toneDesc = toneDescriptions[tone] || toneDescriptions.professional;
  const contentInstructions = contentTypeInstructions[contentType] || contentTypeInstructions.blog;

  return `You are an expert content writer specializing in creating high-quality, engaging content.

Your writing style should be ${toneDesc}.

Task: ${contentInstructions}

Guidelines:
- Write in a clear, engaging manner
- Use proper formatting and structure
- Ensure the content is original and valuable
- Match the requested tone consistently
- Avoid overly generic or templated language
- Focus on quality and relevance`;
}
