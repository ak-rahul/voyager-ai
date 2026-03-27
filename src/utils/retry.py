import time
import random
from functools import wraps
from typing import Callable, Any, Tuple, Type
from src.utils.config import setup_logger

logger = setup_logger(__name__)

def retry_with_backoff(
    retries: int = 3,
    backoff_in_seconds: float = 1.0,
    max_backoff_in_seconds: float = 60.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
) -> Callable:
    """
    Retry decorator with exponential backoff and jitter.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            x = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if x == retries:
                        logger.error(f"Function {func.__name__} failed after {retries} retries. Error: {e}")
                        raise
                    
                    # Exponential backoff with full jitter
                    sleep_time = min(backoff_in_seconds * (2 ** x), max_backoff_in_seconds)
                    jitter = max(0.05, random.uniform(0, sleep_time))
                    
                    logger.warning(
                        f"Retrying {func.__name__} in {jitter:.2f} seconds "
                        f"(Attempt {x + 1}/{retries}) due to error: {e}"
                    )
                    time.sleep(jitter)
                    x += 1
        return wrapper
    return decorator
