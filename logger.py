import logging

logging.basicConfig(
    filename="bot_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_action(user_id, action, message):
    """
    Логирует действия пользователей.
    """
    logging.info(f"User ID: {user_id}, Action: {action}, Message: {message}")
