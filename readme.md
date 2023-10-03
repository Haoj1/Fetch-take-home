# Fetch Rewards Data Engineering Take-Home Assignment

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
  - [Docker and Docker Compose](#docker-and-docker-compose)
  - [Python Dependencies](#python-dependencies)
- [Getting Started](#getting-started)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Start Docker Containers](#2-start-docker-containers)
  - [3. Run the Application](#3-run-the-application)
  - [4. Test local SQL](#4-test-local-SQL)

## Introduction

This application is a small data engineering project designed to demonstrate your ability to read data from an AWS SQS Queue, transform the data, and write it to a PostgreSQL database. It assumes that the evaluator may not have prior experience executing programs in Python. Follow the steps below to set up and run the application.

## Prerequisites

Before running this application, you'll need to install the following prerequisites:

### Docker and Docker Compose

- Docker: Install Docker by following the instructions at [Docker Installation Guide](https://docs.docker.com/get-docker/).

### Python Dependencies

You'll need to install Python dependencies using pip:

```bash
pip install psycopg2-binary l awscli-local
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Haoj1/Fetch-take-home.git
cd Fetch-take-home
```
### 2. Start Docker Containers

```bash
docker-compose up -d
```

### 3. Run the Application
Now you can run the Python application that reads from the AWS SQS Queue, masks PII data, and inserts it into the PostgreSQL database:

```bash
python main.py
```
The application will continuously read messages from the SQS Queue, process them, and insert them into the PostgreSQL database.

### 4. Test local SQL
```bash
psql -d postgres -U postgres -p 5432 -h localhost -W
postgres=# select * from user_logins;
```
Then we can see there are records of userlogin in database table
