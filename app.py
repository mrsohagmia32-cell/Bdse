from flask import Flask, render_template_string, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# ফ্রন্টএন্ড এবং সার্চ ইন্টারফেসের HTML টেমপ্লেট
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>কাস্টম পাইথন সার্চ ইঞ্জিন</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f4f9; margin: 0; padding: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; }
        .container { width: 90%; max-width: 600px; text-align: center; }
        h1 { color: #333; margin-bottom: 20px; }
        .search-box { display: flex; width: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-radius: 30px; overflow: hidden; background: #fff; }
        input[type="text"] { flex: 1; padding: 15px 20px; border: none; outline: none; font-size: 16px; }
        button { padding: 0 25px; background-color: #28a745; color: white; border: none; cursor: pointer; font-size: 16px; }
        button:hover { background-color: #218838; }
        #results { margin-top: 20px; text-align: left; width: 100%; }
        .result-item { background: #fff; padding: 15px; margin-bottom: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .result-item a { color: #007bff; text-decoration: none; font-size: 18px; display: block; margin-bottom: 5px; }
        .result-item a:hover { text-decoration: underline; }
        .result-item p { color: #555; margin: 0; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>সার্ভার-বেসড সার্চ ইঞ্জিন</h1>
        <form method="GET" action="/" class="search-box">
            <input type="text" name="q" placeholder="যেকোনো কিছু সার্চ করুন..." value="{{ query }}">
            <button type="submit">সার্চ</button>
        </form>
        <div id="results">
            {% if results %}
                {% for item in results %}
                    <div class="result-item">
                        <a href="{{ item.url }}" target="_blank">{{ item.title }}</a>
                        <p>{{ item.snippet }}</p>
                    </div>
                {% endfor %}
            {% elif query %}
                <p style="text-align:center;">কোনো ফলাফল পাওয়া যায়নি।</p>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    query = request.args.get('q', '').strip()
    results = []
    
    if query:
        # উদাহরণস্বরূপ DuckDuckGo HTML ভার්শন ক্রল করে ডেটা নিয়ে আসা (সরাসরি ইন্টারনেট সোর্স থেকে)
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            url = f"https://html.duckduckgo.com/html/?q={query}"
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for r in soup.find_all('div', class_='result'):
                    title_tag = r.find('a', class_='result__snippet') or r.find('a', class_='result__url')
                    link_tag = r.find('a', class_='result__url')
                    
                    if title_tag:
                        title = title_tag.get_text().strip()
                        # ইউআরএল বের করা
                        snippet = r.find('a', class_='result__snippet')
                        snippet_text = snippet.get_text().strip() if snippet else "বিবরণ পাওয়া যায়নি"
                        
                        results.append({
                            'title': title,
                            'url': '#',
                            'snippet': snippet_text
                        })
        except Exception as e:
            print(f"Error: {e}")
            
    return render_template_string(HTML_TEMPLATE, results=results, query=query)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
