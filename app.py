from flask import Flask, render_template_string, request
import requests
from bs4 import BeautifulSoup
import urllib.parse

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>আমার ক্রলার সার্চ ইঞ্জিন</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f4f9; margin: 0; padding: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; }
        .container { width: 90%; max-width: 650px; text-align: center; }
        h1 { color: #333; margin-bottom: 20px; }
        .search-box { display: flex; width: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-radius: 30px; overflow: hidden; background: #fff; }
        input[type="text"] { flex: 1; padding: 15px 20px; border: none; outline: none; font-size: 16px; }
        button { padding: 0 25px; background-color: #007bff; color: white; border: none; cursor: pointer; font-size: 16px; }
        button:hover { background-color: #0056b3; }
        #results { margin-top: 20px; text-align: left; width: 100%; }
        .result-item { background: #fff; padding: 15px; margin-bottom: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .result-item a { color: #1a0dab; text-decoration: none; font-size: 18px; display: block; margin-bottom: 5px; }
        .result-item a:hover { text-decoration: underline; }
        .url-text { color: #006621; font-size: 13px; margin-bottom: 5px; word-break: break-all; }
        .snippet-text { color: #4d4d4d; margin: 0; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>লাইভ ক্রলার সার্চ ইঞ্জিন</h1>
        <form method="GET" action="/" class="search-box">
            <input type="text" name="q" placeholder="কী খুঁজতে চান এখানে লিখুন..." value="{{ query }}">
            <button type="submit">সার্চ</button>
        </form>
        <div id="results">
            {% if results %}
                {% for item in results %}
                    <div class="result-item">
                        <a href="{{ item.url }}" target="_blank">{{ item.title }}</a>
                        <div class="url-text">{{ item.url }}</div>
                        <p class="snippet-text">{{ item.snippet }}</p>
                    </div>
                {% endfor %}
            {% elif query %}
                <p style="text-align:center;">দুঃখিত, কোনো ফলাফল পাওয়া যায়নি। আবার চেষ্টা করুন।</p>
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
        try:
            # ক্রলার সক্রিয় করার জন্য প্রপার ব্রাউজার হেডার সেট করা
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9'
            }
            
            # Bing সার্চ ইঞ্জিন ক্রল করে লাইভ ডেটা টেনে আনা (এটি স্ক্র্যাপ করা তুলনামূলক সহজ ও নির্ভরযোগ্য)
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.bing.com/search?q={encoded_query}"
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Bing এর সার্চ রেজাল্ট ট্যাগগুলো ক্রল করা
                for item in soup.find_all('li', class_='b_algo'):
                    title_elem = item.find('h2')
                    link_elem = item.find('a')
                    snippet_elem = item.find('div', class_='b_caption')
                    
                    if title_elem and link_elem:
                        title = title_elem.get_text().strip()
                        link = link_elem.get('href', '#')
                        snippet = snippet_elem.get_text().strip() if snippet_elem else "কোনো বিবরণ পাওয়া যায়নি।"
                        
                        # অপ্রয়োজনীয় লিংক বাদ দিয়ে মূল ফলাফল রাখা
                        if link.startswith('http'):
                            results.append({
                                'title': title,
                                'url': link,
                                'snippet': snippet
                            })
                            
        except Exception as e:
            print(f"Crawler Error: {e}")
            
    return render_template_string(HTML_TEMPLATE, results=results, query=query)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
