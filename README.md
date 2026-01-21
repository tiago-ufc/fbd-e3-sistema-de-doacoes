🎁 Charity & Campaign Management System

A Python-based application designed to bridge the gap between charitable institutions and community needs. This system allows for full management of campaigns, event logistics, and inventory tracking for donated goods.

🚀 Features
🏛️ Institution & Campaign Management

    Create & Edit: Register institutions and set up charity campaigns with specific start and end dates.

    List & Filter: Advanced search for campaigns by name, institution, or date ranges.

    Control: Enable or disable campaigns to manage active fundraising efforts.

📦 Logistics & Inventory

    Goods Management: Track the types of items (food, clothing, hygiene products) being distributed.

    Amount Tracking: Monitor stock levels and quantities allocated to specific people or campaigns.

    Beneficiary Linkage: Record which individuals received specific amounts of goods.

🛠️ Tech Stack

    Language: Python, Java, SQL, YAML, XML.

    UI Framework: Panel / HoloViz

    Database: PostgreSQL

    Data Handling: SQLAlchemy & psycopg2

📊 Database Structure
The system operates on a relational model consisting of three main pillars:

    Users/Institutions: Authentication and profile management.

    Campaigns: The core events linked to specific institutions.

    Inventory/Distribution: The flow of goods from the database to the beneficiary.

🔧 Installation

1.Clone the repository

    git clone https://github.com/tiago-ufc/fbd-e3-sistema-de-doacoes.git
    cd fbd-e3-sistema-de-doacoes

2.Install dependencies

    pip install -r python\requirements.txt

3.Database Setup

    Create a PostgreSQL database.
    Rename your .env.example to .env
    On your .env use the information of your own database to fill all .env values

4.Run the App

    panel serve python/CRUD-panel.ipynb --autoreload
