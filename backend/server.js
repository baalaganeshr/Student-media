const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const morgan = require('morgan');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const cookieParser = require('cookie-parser');
const http = require('http');

const socketio = require('socket.io');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '.env') });

const authRoutes = require('./routes/auth');

const app = express();
const server = http.createServer(app);
const io = socketio(server, { cors: { origin: '*' } });

// Middleware
app.use(cors({ origin: true, credentials: true }));
app.use(express.json());
app.use(cookieParser());
app.use(morgan('dev'));
app.use(helmet());
app.use(rateLimit({ windowMs: 15 * 60 * 1000, max: 100 }));


// Status route for web output
app.get('/api/status', (req, res) => {
  res.json({
    env: {
      PORT: process.env.PORT,
      MONGO_URI: process.env.MONGO_URI,
      CLIENT_URL: process.env.CLIENT_URL,
    },
    mongoConnected: mongoose.connection.readyState === 1,
    server: 'running',
  });
});

// Routes
app.use('/api/auth', authRoutes);

// Socket.io setup
io.on('connection', (socket) => {
  console.log('User connected:', socket.id);
  socket.on('disconnect', () => {
    console.log('User disconnected:', socket.id);
  });
});

// Debug: print environment variables
console.log('ENV:', process.env);
// MongoDB connection
mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => {
  console.log('MongoDB connected');
  server.listen(process.env.PORT || 5000, () => {
    console.log(`Server running on port ${process.env.PORT || 5000}`);
  });
})
.catch((err) => console.error('MongoDB connection error:', err));
