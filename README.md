# CollabTrack: Version-Controlled File Management System for Musicians (MVP)

## Motivation and Description

This project is an **MVP (Minimum Viable Product)** of a web application intended for use by musicians for **version control and collaboration** with audio files. The goal is to replace ad-hoc file sharing with a systematic tracking system built on modern cloud and database technologies.

As a case study in data science and product management, the long-term vision for CollabTrack includes features like human-verification tagging for projects, allowing users to search by human creation status and promoting human-made art in the face of rising AI concerns.

This work was utilized as an opportunity to implement and better familiarize myself with core **database design and cloud computing technologies**.


---

## 🚀 Technical Stack

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend Framework** | Python, **Flask** | Application core, routing, and business logic. |
| **Database** | **PostgreSQL** (Dockerized), SQLAlchemy | Stores all relational metadata (Users, Projects, Version history). |
| **Cloud Storage** | **AWS S3**, **Boto3** | Secure, scalable storage for project files and signed URL generation. |
| **Security** | **Bcrypt**, Python `session`, **DOTENV** | Password hashing, secure session management, and credential protection. |
| **Development** | Git, GitHub | Version control and source code management. |

---

## ✨ Achieved MVP Functionality & Competencies

### 1. Robust User Authentication & Security

* Implemented **secure registration** using `bcrypt` for password hashing.
* Enforced **application security** with a custom **`@login_required` decorator**, ensuring only authenticated users can access core routes.
* Utilized **DOTENV** to keep all sensitive credentials (AWS Keys, database passwords) out of the codebase.

### 2. Full Data Lifecycle (CRUD) Implementation

This section demonstrates the successful implementation of the entire version control workflow:

* **Create/Upload:** Users can create new projects and upload files, saving project metadata to PostgreSQL and the file object to S3.
* **Read/Retrieve (Dashboard):** Implemented a secure **Project Dashboard** that lists the user's projects and a **Project Details** page that queries and displays the full version history (metadata).
* **Download:** Built a secure route that uses **Boto3** to generate **time-limited, pre-signed S3 URLs**, allowing authorized users to safely download specific file versions directly from the cloud.

### 3. Three-Tier Data & Storage Architecture

Designed and implemented a scalable, decoupled storage system:

* **Metadata:** Structured data (version numbers, file names, owner IDs) is stored in **PostgreSQL**.
* **Object Storage:** Large files are securely managed via **AWS S3**, demonstrating competency in cloud infrastructure integration.
* **Versioning Logic:** Custom logic tracks and assigns **sequential version numbers** to files uploaded to the same project.

---

## ⏭️ Next Steps (Polish and Expansion)

The core MVP is complete. The next steps focus on improving the user experience and administrative features:

* **Frontend Templating:** Replace current routes (e.g., `/dashboard`, `/login`) which use plain HTML strings with organized, professional **Jinja templates** for better UI/UX.
* **Landing Page:** Create a simple public `/` route to serve as the application's homepage and direct users to the login/register workflow.