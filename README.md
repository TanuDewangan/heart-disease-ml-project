# heart-disease-ml-project
End-to-end ML project with Streamlit frontend and FastAPI backend.

# Architecture
                         ┌───────────────────────────────┐
                         │         User (Browser)         │
                         │    Streamlit Frontend UI       │
                         └───────────────┬───────────────┘
                                         │  (HTTPS Request)
                                         ▼
                         ┌────────────────────────────────┐
                         │      FastAPI Backend API       │
                         │  - Loads ML Model (.pkl)       │
                         │  - Preprocess Inputs           │
                         │  - Predicts Heart Disease      │
                         └───────────────┬───────────────┘
                                         │
                                         ▼
                         ┌────────────────────────────────┐
                         │    ML Model + Scaler Files     │
                         │  - LR_heart_model.pkl          │
                         │  - heart_scaler.pkl            │
                         │  - heart_columns.pkl           │
                         └────────────────────────────────┘

Render Deployment Flow:
   • Frontend deployed as Streamlit Service
   • Backend deployed as FastAPI Web Service
   • API URL used inside frontend for predictions

# ASCII CI/CD Architecture Diagram

┌──────────────────────────┐
│      Developer           │
│   (Pushes to GitHub)     │
└───────────────┬──────────┘
                │
                ▼
      ┌───────────────────────────────┐
      │     GitHub Actions (CI)       │
      │        python-ci.yml          │
      │-------------------------------│
      │ ✔ Install dependencies        │
      │ ✔ Lint / Syntax check         │
      │ ✔ Validate environment        │
      └───────────────┬──────────────┘
                      │
                      ▼
     ┌───────────────────────────────────────┐
     │     GitHub Actions (CD: Deployment)   │
     └───────────────┬───────────────┬──────┘
                     │               │
                     │               │
                     ▼               ▼

     ┌──────────────────────────┐   ┌──────────────────────────┐
     │   deploy-backend.yml     │   │  deploy-frontend.yml     │
     │--------------------------│   │--------------------------│
     │ ✔ Trigger Render API    │    │  ✔ Trigger Render API   │
     │   to deploy backend      │   │   to deploy frontend     │
     └───────────────┬──────────┘   └──────────────┬──────────┘
                     │                             │
                     ▼                             ▼

   ┌────────────────────────────┐      ┌────────────────────────────┐
   │   Render Backend Service   │      │   Render Frontend Service  │
   │        (FastAPI)           │      │         (Streamlit)        │
   │   /predict endpoint        │      │  Calls backend for result  │
   └───────────────┬────────────┘      └────────────────────────────┘
                   │
                   ▼
        ┌──────────────────────────────┐
        │   ML Artifacts (.pkl files)  │
        │------------------------------│
        │  • LR_heart_model.pkl        │
        │  • heart_scaler.pkl          │
        │  • heart_columns.pkl         │
        └──────────────────────────────┘

This project uses a clean CI/CD pipeline:

🔹 Continuous Integration (CI)
   - python-ci.yml validates code quality, installs dependencies,
     and checks for errors on every push.

🔹 Continuous Deployment (CD)
   - deploy-backend.yml automatically redeploys the FastAPI backend on Render.
   - deploy-frontend.yml automatically redeploys the Streamlit frontend on Render.

🔹 Production Architecture
   - Frontend (Streamlit) sends user inputs to Backend (FastAPI) via /predict API.
   - Backend loads ML model (.pkl), scaler, and feature engineering files.
   - Both services are independently deployed on Render.

# Mermaid Diagram

flowchart TD

A[Developer Pushes Code to GitHub] --> B[GitHub Actions: python-ci.yml<br>CI: Linting, Dependency Check]

B --> C1[deploy-backend.yml<br>Trigger Render Backend Deploy]
B --> C2[deploy-frontend.yml<br>Trigger Render Frontend Deploy]

C1 --> D1[Render Backend Service<br>FastAPI API /predict]
C2 --> D2[Render Frontend Service<br>Streamlit Web UI]

D2 --> D1
D1 --> F[ML Model (.pkl)<br>Scaler + Feature Columns]

               