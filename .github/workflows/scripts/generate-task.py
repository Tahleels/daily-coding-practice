import os, datetime, smtplib, json
from email.mime.text import MIMEText
import google.generativeai as genai

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

today = datetime.date.today().isoformat()
folder = 'solutions'
os.makedirs(folder, exist_ok=True)

# Simple task generation - DSA/Python basics
prompt = f"""
Generate ONE simple coding task for daily practice. Examples:
- Reverse string without built-in methods
- Find duplicates in array O(n)
- Fibonacci with memoization
- Binary search implementation
- Palindrome checker

Return JSON only:
{{
  "title": "Clear title",
  "problem": "1-2 sentences problem",
  "solution": "Complete working Python code",
  "explanation": "2-3 sentences how it works"
}}
Keep under 50 lines total. Use only Python stdlib.
"""

try:
    response = model.generate_content(prompt)
    result = json.loads(response.text.strip('``````'))
    
    # Write solution file
    with open(f'{folder}/day-{today}.py', 'w') as f:
        f.write(f'"""{result["title"]}\n{result["problem"]}\n"""\n\n')
        f.write(result["solution"])
    
    # Write doc
    with open(f'{folder}/day-{today}.md', 'w') as f:
        f.write(f'# Day {today}: {result["title"]}\n\n')
        f.write(f'**Problem**: {result["problem"]}\n\n')
        f.write('## Solution\n``````\n\n')
        f.write(f'## Explanation\n{result["explanation"]}')
    
    # Summary for commit/email
    summary = f'{result["title"]}\nFiles: day-{today}.py, day-{today}.md'
    with open(f'{folder}/LAST_TASK.txt', 'w') as f:
        f.write(summary)
    
    # Email
    msg = MIMEText(f'✅ Daily task complete!\n\n{summary}')
    msg['Subject'] = f'Daily Coding: {result["title"]} - {today}'
    msg['From'] = 'your-email@gmail.com'
    msg['To'] = 'tahleelxmafia@gmail.com'
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('your-email@gmail.com', os.getenv('EMAIL_PASS'))
        server.send_message(msg)
    
    print(f'✅ {summary}')
    
except Exception as e:
    error = f'❌ Error: {str(e)}'
    with open(f'{folder}/LAST_TASK.txt', 'w') as f:
        f.write(error)
    print(error)
