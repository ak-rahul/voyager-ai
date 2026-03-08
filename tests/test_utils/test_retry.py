import pytest
import time
from unittest.mock import patch
from src.utils.retry import retry_with_backoff

def test_retry_success_first_try():
    @retry_with_backoff(retries=3)
    def success_func():
        return "success"
        
    assert success_func() == "success"

@patch('time.sleep', return_value=None)
def test_retry_success_after_failure(mock_sleep):
    call_count = 0
    
    @retry_with_backoff(retries=3, backoff_in_seconds=0.1)
    def flaky_func():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ValueError("Failed")
        return "success"
        
    assert flaky_func() == "success"
    assert call_count == 3
    assert mock_sleep.call_count == 2

@patch('time.sleep', return_value=None)
def test_retry_exhaustion(mock_sleep):
    @retry_with_backoff(retries=2, backoff_in_seconds=0.1)
    def always_fails():
        raise ValueError("Failed repeatedly")
        
    with pytest.raises(ValueError):
        always_fails()
        
    assert mock_sleep.call_count == 2
