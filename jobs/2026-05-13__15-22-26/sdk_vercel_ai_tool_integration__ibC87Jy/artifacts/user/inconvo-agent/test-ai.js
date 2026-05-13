import 'dotenv/config';
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';
import fs from 'fs';

async function main() {
  const { text } = await generateText({
    model: openai('gpt-4o'),
    prompt: 'Hello, say "Total orders: 100"',
  });

  console.log(text);
  fs.writeFileSync('response.json', JSON.stringify({ response: text }));
}

main().catch(console.error);
