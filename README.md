# TomarketBot

**TomarketBot** is a Telegram bot that automates farming, gaming, and daily claiming tasks on the Tomarket platform. It’s built with Python and uses asynchronous programming to handle multiple tasks efficiently.

## Features

### Main Features

- **Farming Management**: Automatically starts farming tasks, checks for completion, and harvests rewards.
- **Game Play & Reward Claim**: Automates game playing on the Tomarket platform, ensuring rewards are claimed when the game points are within a specified range.
- **Daily Rewards**: Automatically claims daily rewards and calculates the next claim time.

## Setup Instructions

### Install `uv`

Before setting up the bot, you need to install `uv`. You can do this globally using pip. Run the following command in your terminal:

```bash
pip install uv
```

### Using `uv`

1. **Clone the Repository**: Open your terminal and run:

   ```bash
   git clone https://github.com/Praveensenpai/TomarketBot.git
   cd TomarketBot
   ```

2. **Sync the Environment**: Run the following command to set up the environment with Python 3.10.2:

   ```bash
   uv sync --python 3.10.2
   ```

3. **Create a `.env` File**: In the project folder, create a file named `.env` and add the following lines:

   ```bash
   SESSION_NAME=<your_session_name>
   API_ID=<your_api_id>
   API_HASH=<your_api_hash>
   REF_ID=<your_referral_id>
   MIN_POINTS=<min_points_for_game>
   MAX_POINTS=<max_points_for_game>
   ```

   - **`SESSION_NAME`**: Choose any name for your session to help the bot remember your login details.
   - **`API_ID`** and **`API_HASH`**: Get these from [my.telegram.org/auth?to=apps](https://my.telegram.org/auth?to=apps) after creating an application.
   - **`REF_ID`**: This is your referral ID, which you can find in your referral link from the Tomarket bot. It will look like this:

     ```
     https://t.me/Tomarket_ai_bot/app?startapp=00019Or9
     ```

     The **`REF_ID`** is the part after `startapp=`, so in this example, it would be `00019Or9`.

   - **`MIN_POINTS`** and **`MAX_POINTS`**: Define the range of points for claiming game rewards.

4. **Run the Bot**: Finally, start the bot by running:

   ```bash
   uv run main.py
   ```

### Alternative Setup Using `pip`

If you prefer using `pip` instead of `uv`, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a Virtual Environment**:

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**:

   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install the Required Packages**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Create a `.env` File**: (same as above)
6. **Run the Bot**:

   ```bash
   python main.py
   ```

## Why Use `uv`?

Using `uv` simplifies managing Python environments by providing better performance and easier setup than traditional virtual environments. Some benefits include:

- **Simplicity**: Easy project setup.
- **Performance**: Faster dependency management.
- **Consistency**: Reduces environment-related issues.

## Usage

- After starting the bot, it will log in to your Telegram account and begin automating tasks like farming and daily claiming.
- Check the logs for the bot’s activity and any errors.

## Contributing

Contributions are welcome! If you have suggestions or improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
