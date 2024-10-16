
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from swarm import Swarm, Agent  # 
import os
import requests

os.environ["OPENAI_API_KEY"] = "sk-lhxs_BlYF4UamdvtPj5Q5RRmgnIOjKxiNiDQ7x0ZxQT3BlbkFJYf4tmYKNFJ9YsUm4B-sHZXquhY3QHQX84IgiZ5O9wA"

# Initialize Swarm client and agents
client = Swarm()

def get_fees_percent():
    url = "https://digitalcurrencypr.com/api/getCommisonTable"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful (status code 200)
        
        # Assuming the API returns JSON data
        data = response.json()
        
        # Process the data and extract the commission table or percentage (based on API response)
        return data  # Replace with specific data extraction if needed
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
def get_fees_under_amount_300():
    "fees under 350 usd is amount - 10, like for 100 usd amount is 90 usd, for 200 amount is 190 usd"

def business_info_agent():
    return Agent(
        name="Business Info Agent",
        instructions=(
            "note that buy for client is sell for us and sell for client is buy for us so in api, buy's fees is sell's fees and sell's fees is buy's fees and also we take -1 usd for network fees"
            "We take a small fee when you exchange fiat to crypto and vice versa. "
            "Fees may change sometimes. If the amount is over $1000, you need to complete a KYC form, "
            "which takes 10-15 minutes. "
            "Company Name is Digital Currency. "
            "The company has 2 branches, both in Georgia Batumi: one in Khimshiashvili and one in Kobaladze."
        ),
        functions=[get_fees_percent,get_fees_under_amount_300],
    )


agent_a = Agent(
    name="Agent A",
    instructions=(
            "note that buy for client is sell for us and sell for client is buy for us so in api, buy's fees is sell's fees and sell's fees is buy's fees and also we take -1 usd for network fees"
        "You are a helpful agent for an offline crypto exchange platform (changing fiat to crypto and vice versa). "
        "Try to give short answers. "
        "You should only respond to messages related to crypto exchange. "
        "If the user's message is not about crypto exchange, politely inform them that you can only assist with "
        "crypto exchange-related queries and end the conversation."
    ),
    functions=[get_fees_percent, business_info_agent, get_fees_under_amount_300],
)

# Dictionary to store user conversation history
user_histories = {}

def is_crypto_related(message):
    crypto_keywords = [
        'crypto', 'cryptocurrency', 'bitcoin', 'ethereum', 'fiat', 'exchange',
        'currency', 'wallet', 'transfer', 'blockchain', 'btc', 'eth', 'hello', 'hi'
    ]
    return any(keyword.lower() in message.lower() for keyword in crypto_keywords)

def handle_message(update, context):
    user_id = update.effective_user.id
    message = update.message.text

    # Retrieve or initialize the user's message history
    history = user_histories.get(user_id, [])
    history.append({"role": "user", "content": message})

    # Run the agent with the conversation history
    response = client.run(
        agent=agent_a,
        messages=history
    )

    # Append the agent's response to the history
    history.append({"role": "assistant", "content": response.messages[-1]["content"]})

    # Update the user's history
    user_histories[user_id] = history

    # Send the agent's response back to the user
    update.message.reply_text(response.messages[-1]["content"])

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("Welcome to the Digital Currency AI Assistant! How can I assist you with crypto exchanges")


def main():
    # Replace 'your-telegram-bot-token' with the token you got from BotFather
    updater = Updater('7358772825:AAFMBLHsx9YssAZh79-6XXC0IFM_JfeAecE', use_context=True)
    dp = updater.dispatcher

    # Handle the /start command
    dp.add_handler(CommandHandler("start", start))

    # Handle messages with the handle_message function
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()