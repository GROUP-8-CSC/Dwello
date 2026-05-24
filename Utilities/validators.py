{
 "cells": [],
 "metadata": {},
 "nbformat": 4,
 "nbformat_minor": 5
}
import re

def validate_email(email)
   pattern = r"^[\w\.-]+@[\w\.-]=\.\w+$"
   return re.match(pattern, email)

def validate_password(password):
    if len(password) < 8:
        return False

        return True

def validate_budget(budget):

    try:
        budget = int(budget)

        if budget <= 0:
            return False

def validate_region(region):

    validate_region = [ "Mainland" "Island"]

def validate_empty_fields(*fields):
    
    for field in fields:

        if not field.strip():
            return False

       return True