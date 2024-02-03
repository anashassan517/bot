from openai import OpenAI
import tkinter as tk
from tkinter import scrolledtext
from tkinter import *
from tkinter import ttk
import os
from dotenv import load_dotenv

load_dotenv()

model = "gpt-3.5-turbo-16k"
system_prompt = "You are a XGen Technology Personalized helpful assistant developed by XGen."

api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    raise ValueError("OPENAI_API_KEY not found in the environment.")

client = OpenAI(api_key=api_key)

messages = [{"role": "system", "content": system_prompt}]
temperature = 0.5

def send_and_receive_message(user_message, messages_temp, temperature=0.5):
    messages_temp.append({"role": "user", "content": user_message})
    
    chat_response = client.chat.completions.create(
        model=model,
        messages=messages_temp,
        temperature=temperature
    )
    
    chat_response_data = chat_response.choices[0].model_dump()["message"]
    chat_response_message = chat_response_data["content"]
    chat_response_role = chat_response_data["role"]

    messages_temp.append({"role": chat_response_role, "content": chat_response_message})
    
    return messages_temp, chat_response_message


def send_message():
    global loading_spinner  # Make the spinner accessible here

    user_input = entry.get()

    # Create and start the loading spinner
    loading_spinner = ttk.Label(root, text="Text Generating Please Be Patient...",font=("Arial",18,'bold'),justify="center")
    loading_spinner.grid(row=1, column=0, sticky="nsew")
    root.update()  # Force GUI update to show the spinner
    
    try:
        messages_list, chat_response = send_and_receive_message(user_input, messages, temperature)

        conversation_history.config(state=tk.NORMAL)
        conversation_history.insert(tk.END, "You: {}\n".format(user_input), "user")
        conversation_history.insert(tk.END, "Bot: {}\n".format(chat_response), "bot")

    except Exception as e:
        conversation_history.insert(tk.END, "Error: {}\n".format(str(e)), "error")

    finally:
        conversation_history.config(state=tk.DISABLED)
        entry.delete(0, tk.END)
        loading_spinner.destroy()  # Remove the spinner after response or error


def quit_application():
    root.destroy()

root = tk.Tk()

# Set window properties
root.title("XGen Bot")

# Set up grid
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

history_label = ttk.Label(root, text="Chat History",font=('bold'))
history_label.grid(row=0, column=0, sticky="nsew")

style = ttk.Style()
style.configure("user.TLabel", foreground="#f8f9fa", font=("Arial", 12, "bold"))
style.configure("bot.TLabel", foreground="#f8f9fa", font=("Arial", 12, "italic"))
style.configure("loading", foreground="#28A745", font=("bold", 20, "italic"))

conversation_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20, font=("Arial", 12))
conversation_history.tag_configure("user", foreground="#007BFF", font=("Arial", 12, "bold"))
conversation_history.tag_configure("bot", foreground="#28A745", font=("Arial", 12, "italic"))
conversation_history.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))


prompt_label = ttk.Label(root, text='Your Message to Bot', font=("Arial", 12,'bold'))
prompt_label.grid(row=2, column=0, pady=5)

entry = Entry(root, font=("Arial", 12))
entry.grid(row=3, column=0, pady=5, sticky="ew")

send_button = Button(root, text="Send", command=send_message, font=("Arial", 12, "bold"), bg="#007BFF", fg="white")
send_button.grid(row=4, column=0, pady=5)

root.mainloop()