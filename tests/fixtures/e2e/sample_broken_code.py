#!/usr/bin/env python3
"""
Sample broken code for testing fix functionality
This file contains intentional bugs for agents to identify and fix
"""


def divide_numbers(a, b):
    """Divide two numbers - has division by zero bug"""
    return a / b  # Bug: No check for b == 0


def get_user_age(users, user_id):
    """Get user age from dictionary - has KeyError bug"""
    return users[user_id]["age"]  # Bug: No check if user_id exists


def process_list(items):
    """Process list items - has IndexError bug"""
    first = items[0]  # Bug: No check if list is empty
    last = items[-1]
    return first, last


def calculate_average(numbers):
    """Calculate average - has division by zero bug"""
    total = sum(numbers)
    return total / len(numbers)  # Bug: No check if numbers is empty


class UserManager:
    """User manager with various bugs"""

    def __init__(self):
        self.users = {}

    def add_user(self, user_id, name):
        """Add user - missing validation"""
        self.users[user_id] = name  # Bug: No validation of inputs

    def get_user(self, user_id):
        """Get user - has KeyError bug"""
        return self.users[user_id]  # Bug: No check if user exists

    def delete_user(self, user_id):
        """Delete user - modifying dict during iteration bug"""
        for uid in self.users:
            if uid == user_id:
                del self.users[uid]  # Bug: Modifying dict during iteration
                break


def main():
    """Test the broken functions"""
    # These will all raise errors
    print(divide_numbers(10, 0))  # ZeroDivisionError
    print(get_user_age({}, "user123"))  # KeyError
    print(process_list([]))  # IndexError
    print(calculate_average([]))  # ZeroDivisionError


if __name__ == "__main__":
    main()
