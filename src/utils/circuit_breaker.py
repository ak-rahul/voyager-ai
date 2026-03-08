import time
from functools import wraps
from typing import Callable, Any
from src.utils.config import setup_logger

logger = setup_logger(__name__)

class CircuitBreakerOpenException(Exception):
    pass

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = "CLOSED"

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if self.state == "OPEN":
                if time.time() - self.last_failure_time > self.recovery_timeout:
                    logger.info("Circuit breaker entering HALF-OPEN state")
                    self.state = "HALF-OPEN"
                else:
                    raise CircuitBreakerOpenException(f"Circuit breaker is OPEN. Fast failing.")
            
            try:
                result = func(*args, **kwargs)
                if self.state == "HALF-OPEN":
                    logger.info("Circuit breaker closed successfully after recovery")
                    self.state = "CLOSED"
                    self.failure_count = 0
                return result
            except Exception as e:
                self.failure_count += 1
                self.last_failure_time = time.time()
                if self.failure_count >= self.failure_threshold:
                    logger.warning(f"Circuit breaker tripped to OPEN state. Error: {e}")
                    self.state = "OPEN"
                raise e
        return wrapper
