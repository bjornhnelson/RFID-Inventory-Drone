# Autonomous RFID Drone For Inventory Tracking
Computer Engineering Senior Project  
By: Chase Earhart, Bjorn Nelson, Caleb Rabbon

# Abstract
With the ongoing rise of e-commerce, warehouses are growing larger in size. Increasing demand for goods means warehouse managers need to know precise details about their inventory, including where it is, how much is in their warehouse, and when items need to be shipped out. A traditional solution to manage inventory is counting and recording it manually with humans and barcode readers, but this leads to human errors such as double counting or missing items. Our solution is an autonomous RFID drone which can quickly and efficiently scan all inventory in a warehouse and accurately display locations of items on a three-dimensional map. An autonomous RFID drone will be able to scan tall shelves and follow designated paths to avoid errors in counting inventory. Our solution utilized the Cal Poly drone, the Cal Poly MiniStock RFID reader, Pozyx positioning hardware and software, and the Python programming language for data acquisition and visualization. Our results allowed us to autonomously fly the Cal Poly drone via GPS, scan and read tags with Cal Poly’s MiniStock, and integrate the Pozyx system with Python to visualize scanned data points. Unfortunately, we were not able to test fly the drone inside a warehouse due to COVID-19. We were also not able to fully integrate all components of the project (drone, Pozyx, data visualization) into a single product due to closure of the RFID lab. It is hoped that our work can be further built on by university students in the future and will help spur adoption of autonomous RFID drones in inventory management.

# Data Management
This software can add or update inventory data stored in a CSV file.
Run command: python3 manageTags.py

# Data Visualization
This software creates a 3D visualization of inventory using the Plotly Python library.

Pozyx data collection run command: python3 localconnect.py
3D visualization run command: python3 finalGraph.py ministockData.csv pozyxData.json output.csv

# Project Documentation
Report: LINK
Video: https://youtu.be/OQxa1KQnF4o
