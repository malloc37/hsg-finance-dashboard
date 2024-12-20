# 📊 Investment Advisor Dashboard

Welcome to the **Investment Advisor Dashboard** – a comprehensive tool to help users **analyze**, **plan**, and **visualize** their investments based on their financial goals and risk preferences.

---

### 📋 About the App

The **Investment Advisor Dashboard** is a Streamlit-powered application that guides users through a step-by-step process to:

1. Input their **initial investment**, **monthly savings**, and **investment term**.
2. Select their **risk tolerance levels** and allocate risk proportions.
3. View personalized **investment options** and **financial metrics**.
4. Analyze **historical price trends**, **market sentiment**, and **projected returns**.
5. Visualize expected **future investment growth** based on user inputs.

---

### 🚀 Features

- **Dynamic User Journey**: The app adjusts the flow based on user inputs.
- **Financial Metrics Dashboard**: Displays key metrics like Market Cap, Volatility, P/E Ratio, and more.
- **Interactive Visuals**:
   - Price trends displayed using **Plotly charts**.
   - Tooltips and information for every financial metric.
   - **Market Sentiment Analysis**: Fetches and analyzes stock-related news sentiment.
   - **Return Calculation**: Computes expected returns for both initial investments and monthly contributions.
   - **User-Friendly Navigation**: Step-by-step navigation ensures a smooth user experience.

---

### 🛠 How to Install and Run

Follow these steps to set up and run the app on your local machine:

1. Clone the Repository
    
    ```bash
    git clone https://github.com/your-username/investment-dashboard.git
    cd investment-dashboard
    ```
2. Install the Required Packages
    
    ```bash
    pip install -r requirements.txt
    ```
   Ensure you have Streamlit, Plotly, yfinance, TextBlob, and other dependencies installed.

3. Run the App
    
    ```bash
    streamlit run app.py
    ```

4. Access the App

	Open the provided Streamlit URL (e.g., http://localhost:8501) in your web browser to start using the dashboard.

--- 
### 📦 Project Structure

The project follows a modular structure for better maintainability:

```plaintext
.
├── app.py                        # Main entry point for the Streamlit app
├── components/
│   ├── input_form.py             # Input form component
│   ├── options_list.py           # Investment options list
│   ├── dashboard.py              # Financial metrics and dashboard
│   ├── openingQuestions.py       # Pages for user inputs (e.g., risk, term)
│   ├── returns.py                # Returns calculation and display
├── data/
│   ├── finance_api.py            # API calls to retrieve financial data
├── utils/
│   ├── styling.py                # Custom CSS and styling utilities
├── requirements.txt              # List of dependencies
└── README.md                     # Project documentation
```

### 🐛 Known Bugs  
- **Double Click Problem**: Currently, some actions in the app require a double click instead of a single click to trigger properly.



