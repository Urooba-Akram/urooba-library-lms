# library_manager.py with Streamlit integration and advanced imports + Custom CSS

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import time
import random
import plotly.express as px
import plotly.graph_objects as graph_objects
from streamlit_lottie import st_lottie
import requests

# Page config
st.set_page_config(
    page_title="📚 Personal Library Management System",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
custom_css = """
<style>
    /* General layout */
    body {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f4f6f8;
    }
    
    /* Titles */
    h1, h2, h3 {
        color: #3b3b3b;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #e3eaf2;
        padding: 1rem;
    }

    /* Buttons */
    div.stButton > button {
        background-color: #0066cc;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }

    div.stButton > button:hover {
        background-color: #004c99;
    }

    /* Markdown */
    .element-container p {
        font-size: 16px;
        color: #333333;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

FILENAME = "library.txt"

# Load or initialize library
def load_library():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            return json.load(f)
    else:
        return [
            {
                "title": "Python Crash Course",
                "author": "Eric Matthes",
                "year": 2019,
                "genre": "Programming",
                "read": False,
                "added_date": "2025-03-11 11:36:40"
            },
            {
                "title": "Automate the Boring Stuff with Python",
                "author": "Fiza Sagar",
                "year": 2011,
                "genre": "Programming",
                "read": True,
                "added_date": "2025-02-15 11:45:40"
            },
            {
                "title": "Fluent Python",
                "author": "Ramalhor",
                "year": 2022,
                "genre": "Programming",
                "read": False,
                "added_date": "2025-02-15 11:45:40"
            },
            {
                "title": "Effective Python",
                "author": "Brett Slatkin",
                "year": 2020,
                "genre": "Programming",
                "read": True,
                "added_date": "2025-02-15 11:45:40"
            }
        ]

# Save library to file
def save_library(library):
    with open(FILENAME, "w") as f:
        json.dump(library, f)

# Add book to library
def add_book(library, title, author, year, genre, read):
    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read,
        "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    library.append(book)
    save_library(library)

# Remove book from library
def remove_book(library, title):
    new_library = [book for book in library if book["title"].lower() != title.lower()]
    if len(new_library) != len(library):
        save_library(new_library)
        return new_library, True
    return library, False

# Search books
def search_books(library, keyword, by):
    keyword = keyword.lower()
    if by == "Title":
        return [book for book in library if keyword in book["title"].lower()]
    else:
        return [book for book in library if keyword in book["author"].lower()]

# Display statistics
def get_statistics(library):
    total = len(library)
    read = sum(1 for book in library if book["read"])
    percent = (read / total * 100) if total else 0
    return total, read, percent

# Main Streamlit UI
st.title("📚 Personal Library Manager")

menu = ["Add Book", "Remove Book", "Search Book", "View All Books", "Statistics"]
choice = st.sidebar.selectbox("Menu", menu)

library = load_library()

if choice == "Add Book":
    st.header("➕ Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1000, max_value=9999, step=1)
    genre = st.text_input("Genre")
    read = st.selectbox("Have you read it?", ["No", "Yes"])

    if st.button("Add Book"):
        if title and author and genre:
            add_book(library, title, author, int(year), genre, read == "Yes")
            st.success(f"Book '{title}' added successfully!")
        else:
            st.error("Please fill in all the fields.")

elif choice == "Remove Book":
    st.header("🗑️ Remove a Book")
    title = st.text_input("Enter the title of the book to remove")
    if st.button("Remove"):
        library, removed = remove_book(library, title)
        if removed:
            st.success(f"Book '{title}' removed successfully!")
        else:
            st.error("Book not found.")

elif choice == "Search Book":
    st.header("🔍 Search Book")
    search_by = st.radio("Search by", ["Title", "Author"])
    keyword = st.text_input("Enter keyword")
    if st.button("Search"):
        results = search_books(library, keyword, search_by)
        if results:
            for i, book in enumerate(results, 1):
                st.markdown(f"**{i}. {book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
        else:
            st.warning("No matching books found.")

elif choice == "View All Books":
    st.header("📖 All Books in Library")
    if library:
        for i, book in enumerate(library, 1):
            st.markdown(f"**{i}. {book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
    else:
        st.info("Your library is empty.")

elif choice == "Statistics":
    st.header("📊 Library Statistics")
    total, read, percent = get_statistics(library)
    st.write(f"Total books: **{total}**")
    st.write(f"Books read: **{read}**")
    st.write(f"Percentage read: **{percent:.1f}%**")
