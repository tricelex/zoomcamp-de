terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.12.0"
    }
  }
}

provider "google" {
  # Configuration options
  project = "data-engineering-zoomcamp-24"
  region  = "europe-west3"
}

resource "google_storage_bucket" "data-lake-bucket" {
  name          = "kingsway-zoomcamp-24-data-lake"
  location      = "EU"
  force_destroy = true

  storage_class               = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }

    condition {
      age = 30
    }
  }

}