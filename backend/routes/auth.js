const express = require('express');
const router = express.Router();
const { register, login, logout, verifyEmail, forgotPassword, resetPassword, getProfile } = require('../controllers/authController');
const { authMiddleware } = require('../middleware/authMiddleware');

router.post('/register', register);
router.post('/login', login);
router.post('/logout', authMiddleware, logout);
router.get('/verify/:token', verifyEmail);
router.post('/forgot-password', forgotPassword);
router.post('/reset-password/:token', resetPassword);
router.get('/profile', authMiddleware, getProfile);

module.exports = router;
