from flask import Flask, request, jsonify
import sqlite3, re, datetime

app = Flask(__name__)

# Database setup
conn = sqlite3.connect('expenses.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS expenses
             (id INTEGER PRIMARY KEY, date TEXT, category TEXT, amount REAL, note TEXT)''')
conn.commit()

def log_expense(text):
    text = text.lower()
    if 'summary' in text:
        c.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        summary = c.fetchall()
        if summary:
            return '\n'.join([f"{cat.capitalize()}: {amt}" for cat, amt in summary])
        return "No expenses logged yet."
    
    # Parse amount and category
    match = re.search(r'(\d+\.?\d*)\s*(?:on)?\s*(\w+)', text)
    if match:
        amount = float(match.group(1))
        category = match.group(2)
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        c.execute("INSERT INTO expenses (date, category, amount, note) VALUES (?, ?, ?, ?)",
                  (date, category, amount, ""))
        conn.commit()
        return f"Logged {amount} in {category}."
    
    return "Could not understand. Try: 'Spent 300 on groceries'."

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    msg = data.get('message', '')
    reply = log_expense(msg)
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)
