const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();

const PORT = process.env.PORT || 3000;
const DATA_FILE = path.join(__dirname, 'posts.json');

app.use(express.json());
app.use(express.static(__dirname));

// পোস্ট পড়ার রুট (গুগল বট এবং ভিজিটরদের জন্য)
app.get('/api/posts', (req, res) => {
    if (!fs.existsSync(DATA_FILE)) {
        return res.json([]);
    }
    const data = fs.readFileSync(DATA_FILE, 'utf8');
    res.json(JSON.parse(data));
});

// নতুন পোস্ট সেভ করার রুট
app.post('/api/posts', (req, res) => {
    const newPost = req.body;
    let posts = [];
    
    if (fs.existsSync(DATA_FILE)) {
        const data = fs.readFileSync(DATA_FILE, 'utf8');
        posts = JSON.parse(data);
    }
    
    posts.unshift(newPost);
    fs.writeFileSync(DATA_FILE, JSON.stringify(posts, null, 2));
    res.json({ success: true, message: "Post published successfully!" });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
