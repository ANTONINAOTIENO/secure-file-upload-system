# Secure File Upload System

## Project Overview
The **Secure File Upload System** automates secure uploads of files to Google Cloud Storage (GCS) with full logging, encryption, and alerting.  
It ensures that all uploaded data is protected and any unauthorized access is monitored in real-time.

---

## Purpose
- Automate file uploads to GCS.
- Enforce security best practices via IAM roles and Customer-Supplied Encryption Keys (CSEK).
- Log all object creation, deletion, and permission-denied attempts.
- Trigger alerts for unauthorized operations.

---

## Architecture

```
Public Bucket → Event Trigger → Cloud Function → Secure Bucket
```

**Components:**
1. **Public Bucket** – Accepts incoming files.
2. **Event Trigger** – Monitors bucket events via Eventarc or Pub/Sub.
3. **Cloud Function** – Moves files securely to the **Secure Bucket** and applies encryption.
4. **Secure Bucket** – Stores encrypted files with restricted access.

**IAM Roles & Permissions:**
- **Cloud Function Service Account** – `storage.objectAdmin` on secure bucket.
- **Project Users** – Limited roles to simulate testing (`storage.objectViewer`, `storage.objects.create` denied).
- **Logging & Monitoring** – Enabled for all object operations.

---

## Security

### Customer-Supplied Encryption Keys (CSEK)
All secure bucket uploads are encrypted with CSEK.  
Example JSON key (obfuscated):

```json
{
  "key_name": "example-key",
  "key_value": "*****REDACTED*****"
}
```

### IAM Policies
- **Public bucket**: limited access (object creation denied for unauthorized users)
- **Secure bucket**: only Cloud Function SA has write permissions
- Logging enabled for every operation.

---

## Setup Instructions

### Clone Repository
```bash
git clone https://github.com/ANTONINAOTIENO/secure-file-upload-system.git
cd secure-file-upload-system
```

### Required Files
- `csek-key.json` – Customer-supplied encryption key
- `move-file-func/` – Cloud Function code
- `alert-policy.json` – Logging/alert policy JSON

---

## Sample Commands

### Uploading a File to Public Bucket
```bash
echo "test file" > test.txt
gsutil cp test.txt gs://public-upload-bucket
```

### Moving a File Securely via Cloud Function
```bash
# Triggered automatically by Eventarc / Pub/Sub
# Cloud Function moves file to secure bucket with encryption
```

### Deleting Files
```bash
gsutil rm gs://secured-storage-bucket/test.txt
# Will fail if user lacks 'storage.objects.delete' permission
```

---

## Logging & Monitoring

### Logs Explorer Queries

**Failed Object Deletion:**
```text
resource.type="gcs_bucket"
resource.labels.bucket_name="secured-storage-bucket"
resource.labels.location="us-central1"
protoPayload.methodName="storage.objects.delete"
```

**Failed Object Creation / Permission Denied:**
```text
resource.type="gcs_bucket"
resource.labels.bucket_name="public-upload-bucket"
protoPayload.status.code=7
```

### Alerts
- Log-based alerts trigger email notifications for unauthorized operations.
- Example: `Object Delete Alert Policy` for the secure bucket.

---

## Folder Structure

```
secure-file-upload-system/
├── alert-policy.json
├── csek-key.json
├── move-file-func/             # Cloud Function code
├── README.md
├── createFile4Delete.txt
├── deny.txt
├── test.txt
├── .gitignore
└── bfg.jar                     # Optional: BFG tool for repo cleanup
```

---

## Credits
- Developed by Antonina Otieno  
- Uses Google Cloud Storage, Cloud Functions, Eventarc, and Pub/Sub
- Inspired by secure file handling best practices

---

## Notes
- Avoid committing large files (>100MB) directly; use Git LFS if necessary.
- Ensure `csek-key.json` is kept secure and **never** committed in plaintext in public repos.
- The Cloud Function automatically handles file transfer and encryption for secure storage.
- Log-based alerts are configured for unauthorized object creation, deletion, and other critical events.
