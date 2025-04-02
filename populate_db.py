#!/usr/bin/env python3

"""
Database Population Script for Cybersecurity Tools Management API

This script populates the database with sample data for testing purposes.
It creates sample users and tools that can be used to test the API functionality.
"""

import os
import sys
from flask import Flask
from models import db, User, Tool
from app import create_app

def populate_database():
    """
    Populate the database with sample data.
    """
    print("Starting database population...")
    
    # Create sample users
    try:
        print("Creating sample users...")
        
        # Check if users already exist to avoid duplicates
        existing_users = User.query.all()
        if existing_users:
            print(f"Found {len(existing_users)} existing users. Skipping user creation.")
        else:
            users = [
                User(username="admin_user", email="admin@example.com"),
                User(username="editor_user", email="editor@example.com"),
                User(username="viewer_user", email="viewer@example.com")
            ]
            
            for user in users:
                db.session.add(user)
            
            db.session.commit()
            print(f"Created {len(users)} sample users.")
        
        # Get all users for reference when creating tools
        all_users = User.query.all()
        
        # Create sample tools
        print("Creating sample tools...")
        
        # Check if tools already exist to avoid duplicates
        existing_tools = Tool.query.all()
        if existing_tools:
            print(f"Found {len(existing_tools)} existing tools. Skipping tool creation.")
        else:
            # Create tools for each user
            tools = [
                # Tools for the first user (admin)
                Tool(
                    name="Nmap", 
                    description="Network scanning tool used to discover hosts and services on a computer network.", 
                    user_id=all_users[0].id
                ),
                Tool(
                    name="Wireshark", 
                    description="Network protocol analyzer that lets you capture and interactively browse the traffic running on a computer network.", 
                    user_id=all_users[0].id
                ),
                
                # Tools for the second user (editor)
                Tool(
                    name="Metasploit", 
                    description="Security project that provides information about security vulnerabilities and aids in penetration testing.", 
                    user_id=all_users[1].id if len(all_users) > 1 else all_users[0].id
                ),
                
                # Tools for the third user (viewer)
                Tool(
                    name="Burp Suite", 
                    description="Integrated platform for performing security testing of web applications.", 
                    user_id=all_users[2].id if len(all_users) > 2 else all_users[0].id
                ),
                Tool(
                    name="OWASP ZAP", 
                    description="Free security tool that helps find security vulnerabilities in web applications.", 
                    user_id=all_users[2].id if len(all_users) > 2 else all_users[0].id
                )
            ]
            
            for tool in tools:
                db.session.add(tool)
            
            db.session.commit()
            print(f"Created {len(tools)} sample tools.")
        
        print("Database population completed successfully!")
        return True
        
    except Exception as e:
        db.session.rollback()
        print(f"Error populating database: {e}")
        return False

if __name__ == "__main__":
    # Create Flask app and push application context
    app = create_app()
    with app.app_context():
        success = populate_database()
        sys.exit(0 if success else 1)