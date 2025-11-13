#!/usr/bin/env python3
"""
Retry Utilities with Exponential Backoff

Provides retry decorators and utilities for API calls with:
- Exponential backoff with jitter
- Rate limit handling
- Specific error handling for Anthropic and GitHub APIs
"""

import time
import random
from functools import wraps
from typing import Callable, Type, Tuple, Optional
import sys


def exponential_backoff_with_jitter(
    attempt: int,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    jitter: bool = True
) -> float:
    """
    Calculate exponential backoff delay with optional jitter

    Args:
        attempt: Current attempt number (0-indexed)
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds
        jitter: Whether to add random jitter

    Returns:
        Delay in seconds
    """
    delay = min(base_delay * (2 ** attempt), max_delay)

    if jitter:
        # Add jitter between 0 and delay
        delay = random.uniform(0, delay)

    return delay


def is_rate_limit_error(exception: Exception) -> bool:
    """
    Check if exception is a rate limit error

    Args:
        exception: Exception to check

    Returns:
        True if rate limit error
    """
    error_str = str(exception).lower()
    error_type = type(exception).__name__

    # Check for common rate limit indicators
    rate_limit_keywords = [
        'rate limit',
        'rate_limit',
        'ratelimit',
        'too many requests',
        '429',
        'quota exceeded',
        'throttle',
    ]

    # Check GitHub specific rate limit
    if error_type == 'RateLimitExceededException':
        return True

    # Check for keywords in error message
    return any(keyword in error_str for keyword in rate_limit_keywords)


def is_retryable_error(exception: Exception) -> bool:
    """
    Check if exception is retryable

    Args:
        exception: Exception to check

    Returns:
        True if error is retryable
    """
    error_str = str(exception).lower()
    error_type = type(exception).__name__

    # Rate limit errors are retryable
    if is_rate_limit_error(exception):
        return True

    # Network/connection errors are retryable
    retryable_types = [
        'ConnectionError',
        'TimeoutError',
        'Timeout',
        'ConnectTimeout',
        'ReadTimeout',
        'HTTPError',
        'RequestException',
        'APIConnectionError',
        'APITimeoutError',
        'InternalServerError',
    ]

    if error_type in retryable_types:
        return True

    # Check for retryable error messages
    retryable_keywords = [
        'connection',
        'timeout',
        'timed out',
        'network',
        'temporary',
        'unavailable',
        'service unavailable',
        '500',
        '502',
        '503',
        '504',
        'internal server error',
        'bad gateway',
        'gateway timeout',
    ]

    return any(keyword in error_str for keyword in retryable_keywords)


def retry_with_exponential_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: int = 2,
    jitter: bool = True,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Optional[Callable[[Exception, int], None]] = None,
    verbose: bool = True
):
    """
    Decorator to retry function with exponential backoff

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds
        exponential_base: Base for exponential calculation
        jitter: Whether to add random jitter
        exceptions: Tuple of exceptions to catch and retry
        on_retry: Optional callback function called on each retry
        verbose: Whether to print retry information

    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)

                except exceptions as e:
                    last_exception = e

                    # Don't retry if not a retryable error
                    if not is_retryable_error(e):
                        if verbose:
                            print(f"❌ Non-retryable error: {type(e).__name__}: {e}")
                        raise

                    # Don't retry if this is the last attempt
                    if attempt >= max_retries:
                        if verbose:
                            print(f"❌ Max retries ({max_retries}) exceeded for {func.__name__}")
                        raise

                    # Calculate delay
                    delay = exponential_backoff_with_jitter(
                        attempt, base_delay, max_delay, jitter
                    )

                    # Special handling for rate limits - use longer delay
                    if is_rate_limit_error(e):
                        delay = max(delay, 30.0)  # At least 30 seconds for rate limits
                        if verbose:
                            print(f"⏳ Rate limit detected, waiting {delay:.1f}s before retry {attempt + 1}/{max_retries}")
                    else:
                        if verbose:
                            print(f"⚠️  {type(e).__name__}: {e}")
                            print(f"🔄 Retrying in {delay:.1f}s (attempt {attempt + 1}/{max_retries})...")

                    # Call on_retry callback if provided
                    if on_retry:
                        try:
                            on_retry(e, attempt)
                        except Exception as callback_error:
                            if verbose:
                                print(f"⚠️  Error in on_retry callback: {callback_error}")

                    # Wait before retrying
                    time.sleep(delay)

            # This shouldn't be reached, but just in case
            if last_exception:
                raise last_exception

        return wrapper
    return decorator


def retry_anthropic_api_call(
    max_retries: int = 3,
    base_delay: float = 2.0,
    max_delay: float = 120.0,
    verbose: bool = True
):
    """
    Specialized retry decorator for Anthropic API calls

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds
        verbose: Whether to print retry information

    Returns:
        Decorated function
    """
    # Import anthropic exceptions if available
    try:
        from anthropic import (
            APIError,
            APIConnectionError,
            APITimeoutError,
            RateLimitError,
            InternalServerError,
        )
        anthropic_exceptions = (
            APIError,
            APIConnectionError,
            APITimeoutError,
            RateLimitError,
            InternalServerError,
            ConnectionError,
            TimeoutError,
        )
    except ImportError:
        # Fallback to generic exceptions
        anthropic_exceptions = (Exception,)

    return retry_with_exponential_backoff(
        max_retries=max_retries,
        base_delay=base_delay,
        max_delay=max_delay,
        jitter=True,
        exceptions=anthropic_exceptions,
        verbose=verbose
    )


def retry_github_api_call(
    max_retries: int = 3,
    base_delay: float = 2.0,
    max_delay: float = 120.0,
    verbose: bool = True
):
    """
    Specialized retry decorator for GitHub API calls

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds
        verbose: Whether to print retry information

    Returns:
        Decorated function
    """
    # Import GitHub exceptions if available
    try:
        from github import GithubException, RateLimitExceededException
        github_exceptions = (
            GithubException,
            RateLimitExceededException,
            ConnectionError,
            TimeoutError,
        )
    except ImportError:
        # Fallback to generic exceptions
        github_exceptions = (Exception,)

    return retry_with_exponential_backoff(
        max_retries=max_retries,
        base_delay=base_delay,
        max_delay=max_delay,
        jitter=True,
        exceptions=github_exceptions,
        verbose=verbose
    )


class RetryableAPICall:
    """
    Context manager for retryable API calls

    Example:
        with RetryableAPICall(max_retries=3) as retry:
            result = retry(api_function, arg1, arg2, kwarg=value)
    """

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 2.0,
        max_delay: float = 120.0,
        verbose: bool = True
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.verbose = verbose

    def __enter__(self):
        return self._call_with_retry

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def _call_with_retry(self, func: Callable, *args, **kwargs):
        """
        Call function with retry logic

        Args:
            func: Function to call
            *args: Positional arguments for function
            **kwargs: Keyword arguments for function

        Returns:
            Function result
        """
        @retry_with_exponential_backoff(
            max_retries=self.max_retries,
            base_delay=self.base_delay,
            max_delay=self.max_delay,
            verbose=self.verbose
        )
        def wrapper():
            return func(*args, **kwargs)

        return wrapper()
