# -*- coding: utf-8 -*-
import os

# Banner
banner = """
===========================================================
██╗  ██╗ █████╗  ██████╗ ███████╗██████╗ ███████╗
██║  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗██╔════╝
███████║███████║██║  ███╗█████╗  ██████╔╝█████╗  
██╔══██║██╔══██║██║   ██║██╔══╝  ██╔═══╝ ██╔══╝  
██║  ██║██║  ██║╚██████╔╝███████╗██║     ███████╗
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝     ╚══════╝
===========================================================
🔹 Advanced Deface Page Generator by Arjun ARZ 🔹
GitHub: CyberKallan | Instagram: @imarjunarz
===========================================================
"""
print(banner)

# User Inputs
title = input("Enter the Title: ")
heading = input("Enter the Heading Text: ")
imagelink = input("Enter Image URL: ")
bgimage = input("Enter Background Image URL: ")
message = input("Enter Your Message (Use <br> for line breaks): ")
textcolor = input("Enter Font Color (e.g., white, red, green): ")
youtube_link = input("Enter YouTube Music URL (Direct Link): ")
contact_email = input("Enter Your Contact Email: ")

# Theme Selection
themes = {
    "1": "Hacker Style",
    "2": "Matrix Rain",
    "3": "Dark Glitch",
    "4": "Cyberpunk Neon",
    "5": "Retro Terminal",
    "6": "Minimal Dark"
}

print("\nSelect a Theme:")
for key, value in themes.items():
    print(f"{key}. {value}")

theme_choice = input("\nEnter Theme Number (1-6): ")
selected_theme = themes.get(theme_choice, "Hacker Style")

# Generate HTML File
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            background: url('{bgimage}') no-repeat center center fixed;
            background-size: cover;
            font-family: 'Orbitron', sans-serif;
            color: {textcolor};
            text-align: center;
        }}
        .container {{
            margin-top: 50px;
        }}
        .contact-btn {{
            padding: 15px 30px;
            font-size: 18px;
            font-weight: bold;
            color: white;
            background: red;
            border: none;
            cursor: pointer;
            margin-top: 20px;
        }}
        .contact-info {{
            display: none;
            margin-top: 20px;
            font-size: 20px;
            color: yellow;
        }}
        .glitch {{
            font-size: 40px;
            text-shadow: 0px 0px 5px red, 0px 0px 10px cyan;
            animation: glitch 1s infinite alternate;
        }}
        @keyframes glitch {{
            0% {{ text-shadow: 2px 2px 5px red, -2px -2px 5px cyan; }}
            100% {{ text-shadow: -2px -2px 5px red, 2px 2px 5px cyan; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1 class="glitch">{heading}</h1>
        <img src="{imagelink}" width="400px">
        <p>{message}</p>
        
        <button class="contact-btn" onclick="showEmail()">Contact Us</button>
        <div class="contact-info" id="contact-info">{contact_email}</div>
    </div>

    <script>
        function showEmail() {{
            document.getElementById("contact-info").style.display = "block";
        }}
    </script>

    <!-- Background Music -->
    <iframe width="0" height="0" src="{youtube_link}?autoplay=1&loop=1" frameborder="0"></iframe>
</body>
</html>
"""

# Save the file
with open("index.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("\n✅ The deface page has been generated as 'index.html' Follow @imarjunarz for more")
