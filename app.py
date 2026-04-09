import streamlit as st

def main():
    st.title("Real Estate Investment Analyzer")
    st.write(
        "Evaluate a rental property by entering purchase, income, and expense details. "
        "The app calculates key investment metrics to help you quickly understand "
        "whether a deal looks promising."
    )

    st.header("Property Inputs")
    left_col, right_col = st.columns(2)

    with left_col:
        purchase_price = st.number_input(
            "Purchase price ($)",
            min_value=0,
            value=250000,
            step=5000,
            help="Enter the expected price of the property.",
        )
        down_payment_percent = st.slider(
            "Down payment (%)",
            min_value=0,
            max_value=100,
            value=20,
            help="Choose how much of the purchase price will be paid up front.",
        )
        monthly_rent = st.number_input(
            "Expected monthly rent ($)",
            min_value=0,
            value=2200,
            step=50,
            help="Estimated monthly rental income from the property.",
        )
        monthly_operating_expenses = st.number_input(
            "Monthly operating expenses ($)",
            min_value=0,
            value=700,
            step=25,
            help="Include taxes, insurance, repairs, management, and other monthly costs.",
        )

    with right_col:
        interest_rate = st.slider(
            "Mortgage interest rate (%)",
            min_value=0.0,
            max_value=12.0,
            value=6.5,
            step=0.1,
            help="Estimated annual interest rate for the loan.",
        )
        vacancy_rate = st.slider(
            "Vacancy rate (%)",
            min_value=0,
            max_value=20,
            value=5,
            help="Expected percentage of time the unit may be vacant.",
        )
        closing_costs = st.number_input(
            "Closing costs ($)",
            min_value=0,
            value=5000,
            step=500,
            help="Estimated one-time acquisition costs.",
        )
        investment_goal = st.selectbox(
            "Primary investment goal",
            ["Balanced return", "Strong cash flow", "Appreciation focus"],
            help="This helps tailor the recommendation message.",
        )

    st.header("Investment Results")

    down_payment = purchase_price * (down_payment_percent / 100)
    loan_amount = purchase_price - down_payment
    gross_annual_rent = monthly_rent * 12
    effective_monthly_rent = monthly_rent * (1 - vacancy_rate / 100)
    annual_gross_income = effective_monthly_rent * 12
    annual_operating_expenses = monthly_operating_expenses * 12
    net_operating_income = annual_gross_income - annual_operating_expenses
    total_cash_invested = down_payment + closing_costs
    monthly_interest_rate = (interest_rate / 100) / 12
    loan_term_months = 30 * 12

    if loan_amount > 0 and monthly_interest_rate > 0:
        monthly_mortgage_payment = loan_amount * (
            monthly_interest_rate
            * (1 + monthly_interest_rate) ** loan_term_months
            / ((1 + monthly_interest_rate) ** loan_term_months - 1)
        )
    elif loan_amount > 0:
        monthly_mortgage_payment = loan_amount / loan_term_months
    else:
        monthly_mortgage_payment = 0

    monthly_cash_flow = (
        effective_monthly_rent - monthly_operating_expenses - monthly_mortgage_payment
    )
    cap_rate = (net_operating_income / purchase_price * 100) if purchase_price else 0
    cash_on_cash_return = (
        (monthly_cash_flow * 12) / total_cash_invested * 100
        if total_cash_invested
        else 0
    )

    if cash_on_cash_return >= 8 and monthly_cash_flow > 0:
        deal_label = "Good deal"
        deal_color = "green"
    elif cash_on_cash_return >= 4 and monthly_cash_flow >= 0:
        deal_label = "Borderline"
        deal_color = "orange"
    else:
        deal_label = "Needs improvement"
        deal_color = "red"

    cash_flow_color = "green" if monthly_cash_flow >= 0 else "red"

    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
    metrics_col1.markdown(
        f"**Monthly Cash Flow**\n\n:<span style='color:{cash_flow_color}; "
        f"font-size: 1.6rem; font-weight: 700;'>${monthly_cash_flow:,.0f}</span>",
        unsafe_allow_html=True,
    )
    metrics_col2.metric("Net Operating Income", f"${net_operating_income:,.0f}")
    metrics_col3.metric("Cap Rate", f"{cap_rate:.2f}%")

    extra_col1, extra_col2 = st.columns(2)
    extra_col1.metric("Estimated Mortgage Payment", f"${monthly_mortgage_payment:,.0f}")
    extra_col2.metric("Cash-on-Cash Return", f"{cash_on_cash_return:.2f}%")

    st.markdown(
        f"**Recommendation Label:** "
        f"<span style='color:{deal_color}; font-weight: 700;'>{deal_label}</span>",
        unsafe_allow_html=True,
    )

    income_col1, income_col2 = st.columns(2)
    income_col1.metric("Gross Annual Rent", f"${gross_annual_rent:,.0f}")
    income_col2.metric("Effective Annual Rent After Vacancy", f"${annual_gross_income:,.0f}")

    if monthly_cash_flow > 0 and cap_rate >= 6:
        recommendation = "This property appears to have solid income potential."
    elif monthly_cash_flow > 0:
        recommendation = "This property produces positive cash flow, but review the cap rate carefully."
    else:
        recommendation = "This deal may need better rent, lower expenses, or a lower purchase price to be attractive."

    if investment_goal == "Strong cash flow" and monthly_cash_flow < 300:
        recommendation += " Since your goal is cash flow, this may not meet your target yet."
    elif investment_goal == "Appreciation focus":
        recommendation += " Appreciation-focused buyers may still consider location and long-term market growth."

    st.subheader("Deal Summary")
    st.write(recommendation)

    st.bar_chart(
        {
            "Amount ($)": {
                "Effective Annual Rent": annual_gross_income,
                "Annual Expenses": annual_operating_expenses,
                "Annual Debt Service": monthly_mortgage_payment * 12,
                "Annual Cash Flow": monthly_cash_flow * 12,
            }
        }
    )

    st.caption(
        "These results are estimates for learning purposes and should be combined with "
        "market research before making an investment decision."
    )

if __name__ == "__main__":
    main()
