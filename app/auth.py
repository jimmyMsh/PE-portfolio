"""
Authentication module for the Flask application.
Provides decorators and utilities for admin authentication.
"""

from functools import wraps
from flask import session, jsonify, request, url_for, render_template, redirect
import secrets
import os

def admin_required(f):
    """
    Decorator to protect routes that require admin authentication.
    
    Args:
        f: The Flask route function to be protected
        
    Returns:
        decorated_function: A wrapper function that checks for admin status
        
    Example:
        @app.route('/admin/dashboard')
        @admin_required
        def admin_dashboard():
            return 'Admin only content'
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user has admin privileges in session
        if not session.get('is_admin'):
            return jsonify({'error': 'Unauthorized access. Admin privileges required.'}), 401
        # If admin, proceed with the original function
        return f(*args, **kwargs)
    return decorated_function

def init_auth(app):
    """
    Initialize authentication routes and configuration for the Flask app.
    
    Args:
        app: Flask application instance
        
    Note:
        Requires ADMIN_PASSWORD and FLASK_SECRET_KEY environment variables
    """
    # Verify required environment variables are set
    if not os.getenv('ADMIN_PASSWORD'):
        raise ValueError('ADMIN_PASSWORD environment variable must be set')
    
    # Set Flask secret key for session management
    app.secret_key = secrets.token_hex(32)
    
    # Register authentication routes
    @app.route('/api/admin/login', methods=['POST'])
    def admin_login():
        """
        Handle admin login requests. Once logged in, session will contain 'is_admin' flag
        that gives access to admin-only functionality across the application.
        
        Expected form data:
            password: Admin password
            
        Returns:
            JSON response indicating success or failure
        """
        # Get password from form submission
        password = request.form.get('password')
        
        # Validate password exists
        if not password:
            return jsonify({'error': 'Password is required'}), 400
            
        # Check if password matches admin password from environment variables
        if password == os.getenv('ADMIN_PASSWORD'):
            # Set admin flag in session - this is what gives admin powers
            session['is_admin'] = True
            return jsonify({'message': 'Login successful'})
        
        return jsonify({'error': 'Invalid password'}), 401
    
    @app.route('/api/admin/logout', methods=['POST'])
    def admin_logout():
        """
        Handle admin logout requests.
        
        Returns:
            JSON response confirming logout
        """
        session.pop('is_admin', None)
        return jsonify({'message': 'Logged out successfully'})
    
    @app.route('/login')
    def login_page():
        """Admin login page route"""
        # If already logged in, redirect to home
        if session.get('is_admin'):
            return redirect(url_for('index'))
        return render_template('login.html', title="Admin Login", active_page='login')