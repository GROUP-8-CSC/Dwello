{
 "cells": [],
 "metadata": {},
 "nbformat": 4,
 "nbformat_minor": 5
}
def format_price(price):

    return f"₦{price:,.0f}"


def capitalize_text(text):

    return text.title()


def truncate_text(text, length=100):

    if len(text) <= length:
        return text

    return text[:length] + "..."