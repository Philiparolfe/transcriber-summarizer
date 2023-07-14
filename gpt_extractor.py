import openai
# Dont forget to enter API key
from keys import MY_KEY
openai.api_key = MY_KEY

MESSAGES=[
        {"role": "system", "content": "You are working as an AI-powered summarization tool, tasked with extracting the key points from an audio transcript. Your goal is to provide a concise summary that captures the main ideas, important details, and relevant insights from the conversation. You have been provided with an audio transcript on [insert topic], and your task is to generate a summary that is no more than [insert word/character limit]. Keep in mind that the summary should be coherent, comprehensive, and reflect the essence of the conversation while omitting redundant or trivial information. Provide a summary that captures the most crucial aspects of the audio transcript, enabling users to grasp the core message efficiently."},
        {"role": "user", "content": "Good Afternoon. This is Olivia speaking. How may I help you? Hello Olivia. My name is William Smith and I’m calling because we have issues with our internet connection. Okay, Sir. Could you please provide me with more details? Sure. During the day our internet is fast but during the nights the connection is very bad. What could cause that? This is because during the nights there is a lot more traffic. What we should do in this case? My suggestion is to send you a new router that will be more powerful. This sounds great. I will inform our technical team to visit you and implement the new router. Okay. Could you please provide me with your address, Mr. Smith? It’s 877 N Frontage Rd, Wisconsin Dells. Thank you. Would next Tuesday at 3 pm suit you? Yes, it’s fine. I will be at home at that time. Great. Thanks for your call, Mr. Smith. Thank you for your time, Olivia. Have a nice day! Thanks. Bye. Bye."},
        {"role": "assistant", "content": "Summary: William Smith called Olivia to report issues with their internet connection, specifically slower speeds during the night. Olivia explained that the problem was likely due to increased internet traffic during that time. She suggested sending a more powerful router to address the issue. William agreed, and Olivia scheduled a visit from the technical team to install the new router. They confirmed the appointment for next Tuesday at 3 pm. The conversation concluded with gratitude and well wishes from both parties."},
        
    ]

def extract(content: str) -> dict:    
    MESSAGES.append({"role": "user", "content": f"{content}"})
    MODEL = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=MESSAGES,
        temperature=0,
    )
    return response['choices'][0]['message']['content']
