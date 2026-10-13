import { NextRequest } from 'next/server';

const GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions';

export async function POST(req: NextRequest) {
  try {
    const { prompt, contentType, tone } = await req.json();

    if (!prompt) {
      return new Response('Prompt is required', { status: 400 });
    }

    const groqApiKey = process.env.GROQ_API_KEY;
    if (!groqApiKey) {
      return new Response('GROQ_API_KEY environment variable is not set.', { status: 500 });
    }
    const modelsToTry = [process.env.GROQ_MODEL || 'qwen/qwen3.8-27b', 'openai/gpt-oss-120b', 'openai/gpt-oss-20b'];

    // Build the system prompt based on content type and tone
    const systemPrompt = buildSystemPrompt(contentType, tone);

    let groqResponse: Response | null = null;
    let lastError = '';

    for (const model of modelsToTry) {
      try {
        const res = await fetch(GROQ_API_URL, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${groqApiKey}`,
            'Content-Type': 'application/json',
            'User-Agent': 'content-gen/1.0',
          },
          body: JSON.stringify({
            model,
            messages: [
              { role: 'system', content: systemPrompt },
              { role: 'user', content: prompt },
            ],
            stream: true,
            temperature: 0.7,
            max_tokens: 600, // kept <= 800 to stay safely under Groq's 1000 OTPM limit
          }),
        });

        if (res.ok) {
          groqResponse = res;
          break;
        } else {
          lastError = await res.text();
          console.warn(`Groq model ${model} failed (${res.status}): ${lastError}. Trying fallback model...`);
        }
      } catch (err: any) {
        lastError = err.message;
      }
    }

    if (!groqResponse || !groqResponse.ok) {
      console.error('All Groq models failed. Last error:', lastError);
      return new Response(
        `AI service rate limit or temporary constraint. Please try again shortly. (${lastError.slice(0, 150)})`,
        { status: 503 }
      );
    }

    // Stream Groq response chunks to client
    const reader = groqResponse.body?.getReader();
    if (!reader) {
      return new Response('Failed to read streaming body', { status: 500 });
    }

    const encoder = new TextEncoder();
    const decoder = new TextDecoder();

    const readableStream = new ReadableStream({
      async start(controller) {
        let buffer = '';
        try {
          while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop() || '';

            for (const line of lines) {
              const trimmed = line.trim();
              if (!trimmed || trimmed === 'data: [DONE]') continue;
              if (trimmed.startsWith('data: ')) {
                try {
                  const json = JSON.parse(trimmed.slice(6));
                  const delta = json.choices?.[0]?.delta?.content || '';
                  if (delta) {
                    controller.enqueue(encoder.encode(delta));
                  }
                } catch {
                  // ignore malformed chunk
                }
              }
            }
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
  } catch (error: any) {
    console.error('Error generating content:', error);
    return new Response(`Error generating content: ${error.message}`, { status: 500 });
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
