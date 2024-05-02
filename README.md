# Vendor Management System

This is a Vendor Management System API developed using Django and REST Framework. It has features to manage vendor profiles, track purchase orders, and calculate vendor performance metrics.

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Project Setup](#Project-Setup)
4. [Features](#Features)
5. [API Documentation](#Api-documentation)
6. [Testing Documenation](#testing-documentation)
7. [Conclusion](#Conclusion)


## Introduction

The Vendor Management System is an API developed using Django and REST Framework. It facilitates the management of vendor profiles, purchase orders, and vendor performance metrics.

## Prerequisites

    -> Python installed on your local machine
    -> Git installed on your local machine
    -> Basic understanding of Django and REST Framework

## Project Setup

    -> Clone Repository:
        Objective: Clone the repository from GitHub.
        Command: git clone <https://github.com/abdul-basith06/Vendor-Management-System.git>

    -> Navigate into Project folder:
        objective: To get inside the project
        command: cd app/Vendor_Management_System    

    -> Install Dependencies:
        Objective: Install project dependencies.(Requirements.txt is inside Vendor_Management_System)
        NB: Activate the env before installing dependencies.(Create one if you don't have)
        Command: pip install -r requirements.txt

    -> Apply Migrations:
        Objective: Apply database migrations.
        Command: python manage.py migrate

    -> Run Development Server
        Objective: Start the development server.
        Command: python manage.py runserver

## Features

    -> Vendor Profile Management: Create, retrieve, update, and delete vendor profiles.
    -> Purchase Order Tracking: Create, retrieve, update, and delete purchase orders, with filtering options by vendor.
    -> Vendor Performance Evaluation: Retrieve performance metrics such as on-time delivery rate, quality rating  average, average response time, and fulfillment rate for vendors.

## API-Documentation

    -> The documentation for Api and it's usage is located in the documentation folder in main directory.(Both swagger and Manual documentation available)

## Testing-Documentation

    -> The documentation for Testing and it's usage is located in the documentation folder in main directory.
    -> The Test files are in tests folder in Project Directory (cd/app/Vendor_Management_System/tests)

## Conclusion

The Vendor Management System simplifies vendor management tasks by providing an intuitive API. By following the setup instructions and exploring its features, users can effectively manage vendors, track purchase orders, and evaluate vendor performance.

