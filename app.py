from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

def parse_datetime(time_str):
  # Try parsing with the format submitted by the form (likely YYYY-MM-DDTHH:MM)
  try:
    return datetime.strptime(time_str, '%Y-%m-%dT%H:%M')
  except ValueError:
    # If parsing fails, try the original format as a fallback
    return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_invoice', methods=['GET', 'POST'])
def create_invoice():
    if request.method == 'POST':
        client_name = request.form['client_name']
        invoice_due = request.form['invoice_due']
        job_description = request.form['job_description']
        start_time = parse_datetime(request.form['start_time'])
        end_time = parse_datetime(request.form['end_time'])
        hourly_rate = float(request.form['hourly_rate'])

        # Calculate total hours worked
        time_diff = end_time - start_time
        total_hours = time_diff.total_seconds() / 3600

        # Calculate total cost
        total_cost = total_hours * hourly_rate

        # Render invoice with calculated values (company_logo argument removed)
        return render_template('invoice.html',
                                client_name=client_name,
                                invoice_due=invoice_due,
                                job_description=job_description,
                                start_time=start_time.strftime('%Y-%m-%d %H:%M:%S'),
                                end_time=end_time.strftime('%Y-%m-%d %H:%M:%S'),
                                hourly_rate=hourly_rate,
                                total_hours=total_hours,
                                total_cost=total_cost)

    return render_template('create_invoice.html')

if __name__ == '__main__':
    app.run(debug=True)