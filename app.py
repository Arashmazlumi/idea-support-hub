import streamlit as st
import sqlite3

# Connect to database
conn = sqlite3.connect('ideas.db')
c = conn.cursor()

# Create table for storing ideas (if table doesn't exist)
c.execute('''
    CREATE TABLE IF NOT EXISTS ideas (
        title TEXT,
        description TEXT,
        support_count INTEGER
    )
''')
conn.commit()

# Website title
st.title("Platform for Supporting Innovative Ideas")

# Form for submitting new ideas
st.header("Register a New Idea")
idea_title = st.text_input("Idea Title:")
idea_description = st.text_area("Description:")

if st.button("Submit Idea"):
    if idea_title and idea_description:
        c.execute('INSERT INTO ideas (title, description, support_count) VALUES (?, ?, ?)',
                  (idea_title, idea_description, 0))
        conn.commit()
        st.success("Your idea has been successfully registered!")
    else:
        st.error("Please enter both the title and description of the idea.")

# Display existing ideas
st.header("Existing Ideas")
c.execute('SELECT rowid, title, description, support_count FROM ideas')
data = c.fetchall()

if data:
    for row in data:
        st.subheader(f"Idea: {row[1]}")
        st.write(f"Description: {row[2]}")
        st.write(f"Number of Supports: {row[3]}")

        if st.button(f"Support {row[1]}", key=row[0]):
            c.execute('UPDATE ideas SET support_count = support_count + 1 WHERE rowid = ?', (row[0],))
            conn.commit()
            st.success(f"You have supported '{row[1]}'!")
else:
    st.write("No ideas have been registered yet.")

# Close database connection
conn.close()
