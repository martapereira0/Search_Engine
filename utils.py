# File to store utility functions to use on the project

import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests


def format_duration(seconds):
    intervals = (
        ('days', 86400),  # 60 * 60 * 24
        ('hours', 3600),  # 60 * 60
        ('minutes', 60),
        ('seconds', 1),
    )

    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            result.append(f"{value} {name}" if value > 1 else f"{value} {name[:-1]}")

    return ', '.join(result)


def show_year_data(df):
    # Count the occurrences of each year
    year_counts = df['year'].value_counts().sort_index()

    # Create a bar chart to display the number of entries per year
    plt.figure(figsize=(10, 6))
    plt.bar(year_counts.index, year_counts.values, color='skyblue')

    # Adding titles and labels
    plt.title('Number of Entries per Year', fontsize=16)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Number of Entries', fontsize=12)

    # Customize x-axis ticks for better readability
    plt.xticks(year_counts.index, rotation=45)

    # Show the plot
    plt.tight_layout()
    plt.show()


def extract_year_from_url(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)
    except requests.exceptions.Timeout:
        return f"Error: Timeout when accessing {url}"
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)} when accessing {url}"

    try:
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # 1. Try to find the year in the original <span class="cit"> pattern
        span_tag_cit = soup.find('span', class_='cit')
        if span_tag_cit:
            raw_date = span_tag_cit.get_text().split(';')[0]
            year = raw_date.split()[0]
            return year

        # 2. Try to find the year in the <span class="fm-vol-iss-date"> pattern
        span_tag_fm = soup.find('span', class_='fm-vol-iss-date')
        if span_tag_fm:
            raw_date = span_tag_fm.get_text().split(' ')[2]  # Extract the year from 'Published online 2008 Apr 15'
            return raw_date

        # 3. Try to find the year in <div class="part1"> within the <div class="fm-citation">
        div_tag_part1 = soup.find('div', class_='part1')
        if div_tag_part1:
            raw_text = div_tag_part1.get_text()
            year = [word for word in raw_text.split() if word.isdigit() and len(word) == 4]
            if year:
                return year[0]  # Return the first match found

        # 4. Try to find the year in <div class="fm-vol-iss-date">
        div_tag_fm_vol = soup.find('div', class_='fm-vol-iss-date')
        if div_tag_fm_vol:
            raw_text = div_tag_fm_vol.get_text()
            year = [word for word in raw_text.split() if word.isdigit() and len(word) == 4]
            if year:
                return year[0]  # Return the first match found

        # 5. Try to find the year in <div class="citation"> pattern
        div_tag_citation = soup.find('div', class_='citation')
        if div_tag_citation:
            raw_text = div_tag_citation.get_text()
            # Extract year, assuming it's the last four-digit number
            year = [word for word in raw_text.split() if word.isdigit() and len(word) == 4]
            if year:
                return year[-1]  # Return the last match found

        return f"Error: Year not found in {url}"

    except Exception as e:
        return f"Error during parsing: {str(e)}"


def preprocessing(df):
    # check if the df has a the colums before applying the preprocessing
    if not 'year' in df.columns:
        df['year'] = df['url'].apply(extract_year_from_url)

    if not 'unique_words' in df.columns:
        df['unique_words'] = df['text'].apply(lambda x: len(set(str(x).split())))

    if not 'n_words' in df.columns:
        df['n_words'] = df['text'].apply(lambda x: len(str(x).split()))

    # TODO: Add more preprocessing steps here
    return df
