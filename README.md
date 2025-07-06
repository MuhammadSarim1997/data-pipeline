# Airflow + Docker + DBT + Airbyte Data Pipeline

This repository contains a modular, end-to-end ELT pipeline that leverages **Airflow**, **Docker**, **DBT**, and **Airbyte** to orchestrate, extract, load, and transform data across Postgres databases.

## 🔧 Tech Stack

- **Apache Airflow**: Workflow orchestration
- **Airbyte**: Data ingestion and syncing between databases
- **Docker Compose**: Containerization and environment management
- **PostgreSQL**: Source and destination databases
- **DBT**: Data transformation and modeling
- **Python**: DAG logic and Airbyte API integration

## 📁 Project Structure

<pre>
data-pipeline/
├── airflow/                  # Airflow config & DAGs
│   ├── dags/
│   │   ├── Airbyte_conection.py
│   │   └── elt_dag.py
│   └── airflow.cfg
├── custom_postgres/          # DBT transformation project
│   ├── dbt_project.yml
│   └── macros/
├── Dockerfile                # Custom Airflow image with providers
├── docker-compose.yml        # Service orchestration
├── source_db_init/           # SQL seed script for source Postgres
├── .env                      # Environment variables
└── .gitignore
</pre>

## ✅ Prerequisites
Make sure the following tools are installed before you run the pipeline:
  - Docker – Required for containerizing all services
  - Docker Compose – For orchestrating multi-container environments
  - abctl (Airbyte CLI) – Used to install and manage Airbyte via Kubernetes-in-Docker (automatically handled via script)
  - Python 3.8+ – Required to run custom Python DAG logic (e.g., API calls to Airbyte)

💡 Tip: No need to manually install Airbyte – the elt.sh script will install it for you using install_abctl.sh.

## ⚙️ Setup Instructions

### 1. Clone the Repository


'''bash
git clone https://github.com/MuhammadSarim1997/data-pipeline.git
cd data-pipeline
bash'''
  
### 2. Add Environment Variables
Create a .env file :

<pre>
AB_client_id="your_airbyte_client_id"
AB_client_secret="your_airbyte_client_secret"
AB_connection_id="your_airbyte_connection_id"
AB_workspace_id="your_airbyte_workspace_id"

POSTGRES_USER=postgres
POSTGRES_PASSWORD=secret
AIRFLOW_DB_USER=airflow
AIRFLOW_DB_PASSWORD=airflow
AIRFLOW_DB_NAME=airflow
AIRFLOW_USERNAME=airflow
AIRFLOW_PASSWORD=password
AIRFLOW_FERNET_KEY=your_fernet_key
</pre>
  
### 3. Build and Start the Pipeline
<pre>
bash ./elt.sh
</pre>
This script:
  - Installs Airbyte via abctl if needed
  - Loads the environment
  - Initializes Airflow
  - Starts Airflow, Airbyte, and Postgres services via Docker

### 4. Access Interfaces
Service	URL
<pre>
Airflow UI	http://localhost:8080
Airbyte UI	http://localhost:8000
Source DB	localhost:5433
Destination DB	localhost:5434
</pre>
## ✅ Features
  - Automated Airbyte syncs via Airflow DAG
  - Polling and job status tracking with Airbyte API
  - Custom transformations using dbt
  - Containerized setup for easy deployment
  
## 📌 TODO
- Add logging and error alerts to DAG
- Extend to S3 or Snowflake
- Set up GitHub Actions for CI/CD

## 📜 License
MIT License — feel free to fork and extend.
