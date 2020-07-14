# Autonomous RFID Drone For Inventory Tracking
Computer Engineering Senior Project - June 2020  
By: Chase Earhart, Bjorn Nelson, Caleb Rabbon  

# Abstract
With the ongoing rise of e-commerce, warehouses are growing larger in size. Increasing demand for goods means warehouse managers need to know precise details about their inventory, including where it is, how much is in their warehouse, and when items need to be shipped out. A traditional solution to manage inventory is counting and recording it manually with humans and barcode readers, but this leads to human errors such as double counting or missing items. Our solution is an autonomous RFID drone which can quickly and efficiently scan all inventory in a warehouse and accurately display locations of items on a three-dimensional map. An autonomous RFID drone will be able to scan tall shelves and follow designated paths to avoid errors in counting inventory. Our solution utilized the Cal Poly drone, the Cal Poly MiniStock RFID reader, Pozyx positioning hardware and software, and the Python programming language for data acquisition and visualization. Our results allowed us to autonomously fly the Cal Poly drone via GPS, scan and read tags with Cal Poly’s MiniStock, and integrate the Pozyx system with Python to visualize scanned data points. Unfortunately, we were not able to test fly the drone inside a warehouse due to COVID-19. We were also not able to fully integrate all components of the project (drone, Pozyx, data visualization) into a single product due to closure of the RFID lab. It is hoped that our work can be further built on by university students in the future and will help spur adoption of autonomous RFID drones in inventory management.

# Data Management
This software can add or update inventory data stored in a CSV file. The attributes are tag ID, description, arrival time, and shipping time. Positional coordinates are calculated by the data visualization software after the drone flies within range of a RFID tag on a piece of inventory.  

Data management run command: python3 manageTags.py  

# Data Visualization
This software creates a 3D graph of inventory, using input files from the MiniStock RFID reader and Pozyx positioning system. The data is processed by finding the indoor positions (x/y/z coordinates in pozyxData.json) associated with the timestamps when RFID tags (tag IDs in ministockData.csv) were read by the drone. The processed data is written to a file (output.csv) and shown using the Plotly Python library.  

Pozyx data collection run command: python3 localconnect.py  

Data visualization run command: python3 finalGraph.py ministockData.csv pozyxData.json output.csv  

# Project Documentation
This section contains the final report and video slides. The video linked below explains the development process and has a demo of the software acquiring Pozyx data and creating a 3D visualization of inventory data.  

Video: https://youtu.be/OQxa1KQnF4o  
