import pytest
import time
from src.utils.circuit_breaker import CircuitBreaker, CircuitBreakerOpenException

def test_circuit_breaker_success():
    cb = CircuitBreaker(failure_threshold=3, recovery_timeout=1)
    
    @cb
    def working_function():
        return "success"
        
    assert working_function() == "success"
    assert cb.state == "CLOSED"

def test_circuit_breaker_failure():
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=1)
    
    @cb
    def failing_function():
        raise ValueError("Intentional failure")
        
    # First failure
    with pytest.raises(ValueError):
        failing_function()
    assert cb.state == "CLOSED"
    assert cb.failure_count == 1
    
    # Second failure triggers OPEN
    with pytest.raises(ValueError):
        failing_function()
    assert cb.state == "OPEN"
    
    # Third call fails fast with CircuitBreakerOpenException
    with pytest.raises(CircuitBreakerOpenException):
        failing_function()

def test_circuit_breaker_recovery():
    cb = CircuitBreaker(failure_threshold=1, recovery_timeout=1) # 1 second recovery
    
    @cb
    def unstable_function(fail: bool):
        if fail:
            raise ValueError("Failure")
        return "success"
        
    # Trip it
    with pytest.raises(ValueError):
        unstable_function(True)
    assert cb.state == "OPEN"
    
    # Wait for recovery timeout
    time.sleep(1.1)
    
    # Next call should be HALF-OPEN then CLOSED if successful
    assert unstable_function(False) == "success"
    assert cb.state == "CLOSED"
