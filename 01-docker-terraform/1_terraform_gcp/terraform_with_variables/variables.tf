variable "project_id" {
  description = "The project ID to deploy to"
  default     = "data-engineering-zoomcamp-24"
}

variable "region" {
  description = "The region to deploy to"
  default     = "europe-west3"
}

variable "location" {
  description = "The location to deploy to"
  default     = "EU"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  #Update the below to what you want your dataset to be called
  default     = "kingsway_zoomcamp_24_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  #Update the below to a unique bucket name
  default     = "kingsway-zoomcamp-24-data-lake"
}

variable "gcs_storage_class" {
  description = "Bucket Stogage Class"
  default     = "STANDARD"
}

