# Use Node.js official image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy frontend files
COPY frontend/ ./

# Expose port 3002
EXPOSE 3002

# Create a simple server script
RUN echo 'const express = require("express"); \
const path = require("path"); \
const app = express(); \
const PORT = 3002; \
\
app.use(express.static("public")); \
app.use(express.static(".")); \
\
app.get("/", (req, res) => { \
  res.sendFile(path.join(__dirname, "public", "figma-design.html")); \
}); \
\
app.listen(PORT, "0.0.0.0", () => { \
  console.log(`StudentMedia server running on http://localhost:${PORT}`); \
});' > server.js

# Install express if not already installed
RUN npm install express

# Start the server
CMD ["node", "server.js"]
