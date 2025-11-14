# CollabTrack: Version-Controlled File Management System for Musicians (MVP)

## Motivation and Description

This project is both a case study of a pain point/modern issue and a Minimum Viable Product (MVP) of a web application. As a data science student involved in music as an undergraduate student, I was interested in potential applications musicians would use that could also address rising concerns of AI in the modern day. I did some brief internet research to find a product musicians would use and came up with this. Intended for use by musicians for version control and collaboration with audio files, I designed an app to provide secure, version-controlled file storage for collaborative projects. It replaces ad-hoc file sharing with a systematic tracking system built on modern cloud and database technologies. My vision, if this product were to be launched, includes allowing projects to be tagged with human verification badges, so as to allow users to search for projects by human verification, hopefully encouraging human-made music/art


---

## Technical Stack

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend Framework** | Python, **Flask** | Application core, routing. |
| **Database** | **PostgreSQL** (Dockerized), SQLAlchemy | Stores all relational metadata (Users, Projects, Version history). |
| **Cloud Storage** | **AWS S3**, **Boto3** | Secure, scalable storage for project files. |
| **Security** | **Bcrypt**, Python `session` | Password hashing and secure session management. |
| **Development** | Git, GitHub | Version control and secure environment configuration. |

---

## Key Features & Competencies

### 1. Robust User Authentication & Security

* Implemented **secure registration** using `bcrypt` for password hashing.
* Enforced **application security** with a custom `@login_required` decorator, ensuring only authenticated users can access core routes like project creation and file upload.
* Utilized **DOTENV** to keep all sensitive credentials (AWS Keys, database passwords) out of the codebase.

### 2. Three-Tier Data & Storage Architecture

Designed and implemented a scalable, decoupled storage system:
* **Metadata:** Structured data (version numbers, file names, owner IDs) is stored in **PostgreSQL**.
* **Object Storage:** Large files are securely managed via **AWS S3**, demonstrating competency in cloud infrastructure integration.
* **Versioning Logic:** Custom logic tracks and assigns **sequential version numbers** to files uploaded to the same project, enabling future audit and rollback features.

### 3. Core MVP Functionality

* **Project Management:** Users can create and own multiple projects.
* **Version Control:** Allows users to upload new file versions to existing projects, with each upload recorded with a unique S3 key, file name, and timestamp.

---

## Next Steps

The following features will complete the MVP cycle:

* **Project Dashboard:** Create a route to list a user's projects and view detailed version history (metadata retrieval).
* **File Download:** Implement a secure route to retrieve and serve specific versions from AWS S3 to the user's browser.