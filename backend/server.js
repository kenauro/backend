const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
const port = process.env.port || 8080;

// Middleware to parse JSON bodies
app.use(express.json());
app.use(cors());

// Endpoint to handle /predict
app.post('/predict', async (req, res) => {
    try {
        // Forward the request body to the external API
        const response = await axios.post('https://my-api-2vs6aumwoq-et.a.run.app/predict', req.body);
        
        // Send back the response from the external API
        res.json(response.data);
    } catch (error) {
        // Handle errors appropriately
        if (error.response) {
            res.status(error.response.status).json(error.response.data);
        } else {
            res.status(500).json({ error: 'Something went wrong' });
        }
    }
});


app.post('/predict2', async (req, res) => {
    try {
        // Forward the request body to the external API
        
        const response = await axios.post('https://my-api-2vs6aumwoq-et.a.run.app/predict2', req.body);
        
        // Send back the response from the external API
        res.json(response.data);
    } catch (error) {
        // Handle errors appropriately
        if (error.response) {
            res.status(error.response.status).json(error.response.data);
        } else {
            res.status(500).json({ error: 'Something went wrong' });
        }
    }
});


app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
