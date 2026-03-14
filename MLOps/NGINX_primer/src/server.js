/**
 * server.js - A Scalable, Container-Aware Node.js Web Server
 * * Features:
 * - Dynamic port and app name via Environment Variables
 * - Instance tracking via Docker HOSTNAME (Container ID)
 * - Environment-based security (NODE_ENV) to hide internal headers in production
 */

// Import core Node.js modules
const http = require('http');
const fs = require('fs');
const path = require('path');

// --- Configuration & Environment Setup ---
const PORT = process.env.PORT || 3000;
const APP_NAME = process.env.APP_NAME || "default-app";

// In Docker, HOSTNAME defaults to the Container ID (for debugging)
const instanceName = process.env.HOSTNAME || "unknown-instance";

// Security toggle: check if we are in development mode
const isDev = process.env.NODE_ENV === 'development';

console.log(`Starting instance: ${APP_NAME}`);

// --- Server Logic ---
const server = http.createServer((req, res) => {
    // Construct the absolute path to index.html
    const filePath = path.join(__dirname, 'index.html');

    /**
     * Read the HTML file from the disk.
     * Note: 'utf8' is used so 'data' returns as a string, making it 
     * easier to manipulate if we decide to inject variables later.
     */
    fs.readFile(filePath, 'utf8', (err, data) => {
        // Handle file-not-found or permission errors
        if (err) {
            console.error(`[Error] Could not read file: ${err.message}`);
            res.writeHead(500, { 'Content-Type': 'text/plain' });
            return res.end('Internal Server Error');
        }

        // Initialize standard response headers
        const headers = { 
            'Content-Type': 'text/html',
            'X-App-Name': APP_NAME // General app identification
        };

        /**
         * SECURITY LAYER: 
         * Only expose the specific Container/Instance ID if we are 
         * explicitly in development mode to prevent information leakage.
         */
        if (isDev) {
            // this helps us identify which container served the request during development/testing
            headers['X-Backend-Server'] = instanceName; 
        }

        // Send successful response
        res.writeHead(200, headers);
        res.end(data);
    });
});


// --- Start Server ---
server.listen(PORT, () => {
    console.log(`[${APP_NAME} - ${instanceName}] Service online on port ${PORT} (Mode: ${process.env.NODE_ENV || 'not set'})`);
    console.log(`[${APP_NAME} - ${instanceName}] URL: http://localhost:${PORT}`);
});