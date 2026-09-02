const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware to parse JSON data
app.use(express.json());

// Temporary memory database (Can be replaced with MongoDB or PostgreSQL later)
let playerDatabase = {};

// Root endpoint for health check
app.get('/', (req, res) => {
    legends = { status: "Server is running smoothly on Render!" };
    res.json(legends);
});

// Save or Update Player Game Data
app.post('/api/player/save', (req, res) => {
    const { userId, gameData } = req.body;
    
    if (!userId) {
        return res.status(400).json({ success: false, message: "User ID is required" });
    }

    playerDatabase[userId] = {
        ...gameData,
        lastUpdated: Date.now()
    };

    console.log(`Data saved for user: ${userId}`);
    res.json({ success: true, message: "Game data synced successfully." });
});

// Load Player Game Data
app.get('/api/player/load/:userId', (req, res) => {
    const { userId } = req.params;
    
    if (!playerDatabase[userId]) {
        return res.status(404).json({ success: false, message: "Player data not found." });
    }

    res.json({ success: true, data: playerDatabase[userId] });
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
