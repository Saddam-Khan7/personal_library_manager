import streamlit as st
import os



# ---------- Load & Save ----------
def load_library(filename):
    library = []
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 5:
                    title, author, year, genre, read = parts
                    library.append({
                        'title': title,
                        'author': author,
                        'year': int(year),
                        'genre': genre,
                        'read': read == 'True'
                    })
    return library

def save_library(library, filename):
    with open(filename, 'w') as file:
        for book in library:
            line = f"{book['title']}|{book['author']}|{book['year']}|{book['genre']}|{book['read']}\n"
            file.write(line)

# ---------- App Starts ----------
st.set_page_config(page_title="📚 Personal Library Manager", layout="centered")
st.title("📚 Personal Library Manager")

# Load data
FILENAME = "library.txt"
if "library" not in st.session_state:
    st.session_state.library = load_library(FILENAME)

# ---------- Sidebar Navigation ----------
st.sidebar.markdown("Developed by **Saddam Khan**")
menu = st.sidebar.radio("Navigate", [
    "Add a Book", 
    "Remove a Book", 
    "Search a Book", 
    "Display All Books", 
    "Display Statistics"
])

# ---------- Add Book ----------
if menu == "Add a Book":
    st.subheader("➕ Add a New Book")
    with st.form("add_book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year")
        genre = st.text_input("Genre")
        read = st.radio("Have you read it?", ("Yes", "No")) == "Yes"
        submitted = st.form_submit_button("Add Book")

        if submitted:
            st.session_state.library.append({
                'title': title,
                'author': author,
                'year': year,
                'genre': genre,
                'read': read
            })
            save_library(st.session_state.library, FILENAME)
            st.success("Book added successfully!")

# ---------- Remove Book ----------
elif menu == "Remove a Book":
    st.subheader("❌ Remove a Book")
    titles = [book['title'] for book in st.session_state.library]
    if titles:
        to_remove = st.selectbox("Select a book to remove", titles)
        if st.button("Remove"):
            st.session_state.library = [book for book in st.session_state.library if book['title'] != to_remove]
            save_library(st.session_state.library, FILENAME)
            st.success(f"'{to_remove}' removed successfully.")
    else:
        st.info("Library is empty.")

# ---------- Search ----------
elif menu == "Search a Book":
    st.subheader("🔍 Search for a Book")
    search_by = st.radio("Search by", ("Title", "Author"))
    query = st.text_input("Enter search term")
    if query:
        results = []
        for book in st.session_state.library:
            if search_by == "Title" and query.lower() in book['title'].lower():
                results.append(book)
            elif search_by == "Author" and query.lower() in book['author'].lower():
                results.append(book)

        if results:
            st.write("### Matching Books:")
            for book in results:
                st.markdown(f"- **{book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
        else:
            st.warning("No matching books found.")

# ---------- Display All ----------
elif menu == "Display All Books":
    st.subheader("📖 Your Library")
    if st.session_state.library:
        for book in st.session_state.library:
            st.markdown(f"- **{book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '❌ Unread'}")
    else:
        st.info("Your library is empty.")

# ---------- Statistics ----------
elif menu == "Display Statistics":
    st.subheader("📊 Library Statistics")
    total = len(st.session_state.library)
    read_count = sum(1 for book in st.session_state.library if book['read'])
    percentage = (read_count / total * 100) if total else 0

    st.metric("Total Books", total)
    st.metric("Books Read", f"{percentage:.1f}%")




