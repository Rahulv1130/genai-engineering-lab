import dotenv from 'dotenv';
import OpenAI from "openai";
import Groq from 'groq-sdk'
import promptSync from 'prompt-sync';
import NodeCache from 'node-cache'
import { tavily } from "@tavily/core";
const input = promptSync();
dotenv.config();

const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });
const tvly = tavily({ apiKey: process.env.TAVILY_API_KEY });

const myCache = new NodeCache({stdTTL: 60*60});

export async function getGroqChatCompletion(question, threadId) {

    const baseMessages = [
        {
            role: "system",
            content: `You are Jarvis, a personal assistant who answers the asked questions. If you receive some message that you are unable to understand you can simply give the response back that you need more clarification on the input. If you dont have information about somoething then
                        You have access to the following tools which you should use only if needed:
                    1. webSearch({query} : {query : string}) // Search the Latest Information and realtime data on the internet.`
        }
    ]

    const messages = myCache.get(threadId) ?? baseMessages;
    messages.push({
            role: "user",
            content: question,
        }   )

    try {

        const MAX_RETRIES = 10;
        let count = 0;

        while(true) {

            if(count > MAX_RETRIES) {
                return "Sorry, I could Not Find what you were looking for....!!"
            }
            count++;

            const completions = await groq.chat.completions.create({
                messages: messages,
                tools: [
                    {
                        type: "function",
                        function: {
                            name: "webSearch",
                            description: "Search the Latest Information and realtime data on the internet",
                            parameters: {
                            type: "object",
                            properties: {
                                query: {
                                    type: "string",
                                    description: "The Search Query to perform on the Internet"
                                }
                            },
                            required: ["query"]
                            }
                        }
                    }
                ],
                temperature: 0,
                tool_choice: 'auto',
                model: "llama-3.3-70b-versatile",
            });

            messages.push(completions.choices[0].message)
            const tools = completions.choices[0].message.tool_calls;

            if(!tools) {
                myCache.set(threadId, messages);
                return completions.choices[0].message.content;
            }

            
            for(const tool of tools) {
                const functionName = tool.function.name;
                const functionParams = tool.function.arguments;

                if(functionName === "webSearch") {
                    const toolResult = await webSearch(JSON.parse(functionParams));

                    messages.push(
                        {
                            role: "tool",
                            tool_call_id: tool.id,
                            name: functionName,
                            content: toolResult
                        }
                    );
                }
            }
        } 
    }
    catch(e) {
        return "Sorry! My Bad, Can you please modify your query....."
    }   
}


async function webSearch({query}) {
    console.log("Attempting Web Search....\n")
    const response = await tvly.search(`Give concise info about: ${query}`);
    const finalResponse = response.results.map(el => el.content).join('\n\n');
    return finalResponse;
}

export async function generate(query, threadId) {
    return await getGroqChatCompletion(query, threadId);
}