import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# Define the start and end dates
START_DATE = datetime(2023, 10, 16)
END_DATE = datetime(2023, 12, 31)

# Define the list of tasks
TASKS = [
    "Exercise (Morning)",
    "Meditation",
    "Library",
    "GenAI Project",
    "Kaggle",
    "DSA (1 Chapter Only)",
    "AI (3 hours)",
    "Exercise (Evening)",
    "Brahmacharya"
]

# CSV file to store progress
DATA_FILE = "routine_tracker.csv"

def initialize_data(file_path):
    """Initialize the CSV file with dates and tasks."""
    date_range = pd.date_range(start=START_DATE, end=END_DATE)
    data = {
        "Date": date_range.strftime('%Y-%m-%d'),
        "Day": date_range.strftime('%A')
    }
    for task in TASKS:
        data[task] = False  # Initialize all tasks as not completed
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    return df

def load_data(file_path):
    """Load existing data or initialize if file does not exist."""
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        # Ensure all required columns are present
        expected_columns = ["Date", "Day"] + TASKS
        for col in expected_columns:
            if col not in df.columns:
                df[col] = False
        return df
    else:
        return initialize_data(file_path)

def save_data(df, file_path):
    """Save the DataFrame to CSV."""
    df.to_csv(file_path, index=False)

def main():
    st.set_page_config(page_title="Winter Arc Routine Tracker", layout="wide")
    st.title("❄️ Winter Arc Routine Tracker ❄️")
    st.markdown(f"**Tracking Period:** {START_DATE.strftime('%d %b %Y')} to {END_DATE.strftime('%d %b %Y')}")

    # Load or initialize data
    df = load_data(DATA_FILE)

    # Sidebar for navigation (only "View & Update Tasks" since "Progress Overview" is removed)
    st.sidebar.header("Navigation")
    options = ["View & Update Tasks"]
    choice = st.sidebar.selectbox("Go to", options)

    if choice == "View & Update Tasks":
        st.header("📅 Daily Tasks")

        # Iterate through each row (day) in the DataFrame
        for idx, row in df.iterrows():
            date_str = row["Date"]
            day_str = row["Day"]
            date_display = datetime.strptime(date_str, '%Y-%m-%d').strftime('%d %b %Y')
            
            # Check if all tasks for the day are completed
            all_completed = all(row[task] for task in TASKS)
            
            if all_completed:
                # Append a green checkmark if all tasks are completed
                expander_label = f"**{date_display} - {day_str}** ✅"
            else:
                # Regular expander label without checkmark
                expander_label = f"**{date_display} - {day_str}**"
            
            # Create the expander with the label
            with st.expander(expander_label, expanded=False):
                # For each task, create a checkbox
                for task in TASKS:
                    key = f"{date_str}_{task}"
                    # Set the default state based on the CSV
                    checked = bool(row[task])
                    new_value = st.checkbox(task, value=checked, key=key)
                    if new_value != checked:
                        df.at[idx, task] = new_value
                        save_data(df, DATA_FILE)
                        st.success(f"Updated **{task}** for {date_display}")
                
                # After updating tasks, check if all tasks are completed
                if all(df.loc[idx, task] for task in TASKS):
                    st.markdown(
                        "<div style='color: green; font-weight: bold;'>All tasks completed for this day! ✅</div>",
                        unsafe_allow_html=True
                    )

if __name__ == "__main__":
    main()
