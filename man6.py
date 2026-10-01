import streamlit as st
import json
import os
from datetime import date

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)

FILE_NAME = "expenses.json"


# -----------------------------
# Attractive CSS
# -----------------------------
st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f4f7fb;
    }

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: bold;
        text-align: center;
        color: #2563eb;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 18px;
        margin-bottom: 30px;
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        padding: 20px;
        border-radius: 15px;
        color: white;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
    }

    div[data-testid="metric-container"] label {
        color: white !important;
    }

    div[data-testid="metric-container"] div {
        color: white !important;
    }

    /* Section headings */
    h2 {
        color: #1e3a8a;
    }

    /* Buttons */
    .stButton > button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 20px;
        font-weight: bold;
    }

    .stButton > button:hover {
        background-color: #1d4ed8;
        color: white;
    }

    /* Form */
    div[data-testid="stForm"] {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0px 3px 12px rgba(0,0,0,0.1);
    }

    /* Expense rows */
    .expense-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
    }

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Load Expenses
# -----------------------------
def load_expenses():

    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)

    except:
        return []


# -----------------------------
# Save Expenses
# -----------------------------
def save_expenses(expenses):

    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)


# -----------------------------
# Session State
# -----------------------------
if "expenses" not in st.session_state:
    st.session_state.expenses = load_expenses()


# -----------------------------
# Title
# -----------------------------
st.markdown(
    '<div class="main-title">💰 Expense Tracker</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Track your daily expenses easily and smartly 📊</div>',
    unsafe_allow_html=True
)


# -----------------------------
# Add Expense
# -----------------------------
st.header("➕ Add New Expense")

with st.form("expense_form"):

    col1, col2 = st.columns(2)

    with col1:

        expense_date = st.date_input(
            "📅 Date",
            value=date.today()
        )

        category = st.selectbox(
            "🏷️ Category",
            [
                "Food",
                "Travel",
                "Shopping",
                "Education",
                "Bills",
                "Entertainment",
                "Other"
            ]
        )

    with col2:

        description = st.text_input(
            "📝 Description"
        )

        amount = st.number_input(
            "💵 Amount (₹)",
            min_value=0.0,
            step=1.0
        )

    submitted = st.form_submit_button(
        "➕ Add Expense"
    )

    if submitted:

        if amount <= 0:

            st.error("⚠️ Please enter a valid amount.")

        elif description.strip() == "":

            st.error("⚠️ Please enter a description.")

        else:

            new_expense = {
                "id": len(st.session_state.expenses) + 1,
                "date": str(expense_date),
                "category": category,
                "description": description,
                "amount": amount
            }

            st.session_state.expenses.append(new_expense)

            save_expenses(
                st.session_state.expenses
            )

            st.success(
                "✅ Expense added successfully!"
            )


# -----------------------------
# Summary
# -----------------------------
st.header("📊 Expense Summary")

expenses = st.session_state.expenses

if expenses:

    total_expense = sum(
        expense["amount"]
        for expense in expenses
    )

    number_of_expenses = len(expenses)

    average_expense = (
        total_expense / number_of_expenses
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💰 Total Expense",
        f"₹{total_expense:.2f}"
    )

    col2.metric(
        "🧾 Transactions",
        number_of_expenses
    )

    col3.metric(
        "📈 Average Expense",
        f"₹{average_expense:.2f}"
    )

else:

    st.info(
        "📭 No expenses added yet."
    )


# -----------------------------
# All Expenses
# -----------------------------
st.header("📋 All Expenses")

if expenses:

    for expense in expenses:

        col1, col2, col3, col4, col5 = st.columns(
            [1, 2, 3, 2, 1]
        )

        col1.write(
            f"**#{expense['id']}**"
        )

        col2.write(
            f"📅 {expense['date']}"
        )

        col3.write(
            f"🏷️ {expense['category']} - "
            f"{expense['description']}"
        )

        col4.write(
            f"💵 ₹{expense['amount']:.2f}"
        )

        if col5.button(
            "🗑️ Delete",
            key=f"delete_{expense['id']}"
        ):

            st.session_state.expenses.remove(
                expense
            )

            save_expenses(
                st.session_state.expenses
            )

            st.success(
                "✅ Expense deleted!"
            )

            st.rerun()

else:

    st.info(
        "📭 No expenses available."
    )


# -----------------------------
# Category Chart
# -----------------------------
st.header("📈 Category-wise Expenses")

if expenses:

    category_total = {}

    for expense in expenses:

        category = expense["category"]
        amount = expense["amount"]

        if category not in category_total:
            category_total[category] = 0

        category_total[category] += amount

    st.bar_chart(
        category_total
    )

else:

    st.info(
        "📊 Add expenses to see the chart."
    )


# -----------------------------
# Footer
# -----------------------------
st.markdown("---")

st.markdown(
    "<center>💙 Expense Tracker | "
    "Built with Python & Streamlit</center>",
    unsafe_allow_html=True
)
