"""
ShareMyMeal Backend — Firebase Admin SDK Initialization
========================================================
Initializes the Firebase Admin SDK once at startup.
Provides helper functions to access Firestore, Auth, Storage, and FCM.

Supports two credential sources:
1. FIREBASE_SERVICE_ACCOUNT_JSON env var (for cloud deployment like Render)
2. Local file path (for local development)
"""

import firebase_admin
from firebase_admin import credentials, firestore, auth, storage, messaging
from app.config import settings
import os
import json


def init_firebase():
    """
    Initialize Firebase Admin SDK with service account credentials.
    This should be called once at application startup.

    Priority:
    1. FIREBASE_SERVICE_ACCOUNT_JSON env var (JSON string)
    2. Local file at firebase_service_account_path
    """
    # Prevent re-initialization if already done
    if firebase_admin._apps:
        return

    storage_bucket = "sharemymeal-ed8fc.firebasestorage.app"

    # Option 1: Try loading from environment variable (for cloud deployment)
    service_account_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT_JSON")
    if service_account_json:
        try:
            cred_dict = json.loads(service_account_json)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, {
                "storageBucket": storage_bucket,
            })
            print("✅ Firebase Admin SDK initialized from environment variable.")
            return
        except json.JSONDecodeError as e:
            print(f"⚠️  Failed to parse FIREBASE_SERVICE_ACCOUNT_JSON: {e}")
        except Exception as e:
            print(f"⚠️  Failed to initialize from env var: {e}")

    # Option 2: Try loading from file path (for local development)
    sa_path = settings.firebase_service_account_path
    if os.path.exists(sa_path):
        cred = credentials.Certificate(sa_path)
        firebase_admin.initialize_app(cred, {
            "storageBucket": storage_bucket,
        })
        print("✅ Firebase Admin SDK initialized from file.")
        return

    # Option 3: Try Application Default Credentials
    print(f"⚠️  Service account not found (env var or file: {sa_path})")
    print("   Attempting to initialize with default credentials...")
    try:
        firebase_admin.initialize_app()
        print("✅ Firebase Admin SDK initialized with default credentials.")
    except Exception as e:
        print(f"❌ Firebase initialization failed: {e}")
        print("   The app will run but Firebase features will not work.")
        print("   Please provide a valid service account JSON.")


def get_firestore_client():
    """Get the Firestore database client."""
    return firestore.client()


def get_auth():
    """Get the Firebase Auth instance."""
    return auth


def get_storage_bucket():
    """Get the Firebase Storage bucket."""
    return storage.bucket()


def get_messaging():
    """Get the Firebase Cloud Messaging instance."""
    return messaging
