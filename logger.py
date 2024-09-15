import logging

logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def log_inference_time(user_id: str, inference_time: float):
    logging.info(f"User: {user_id}, Inference Time: {inference_time:.4f}s")
