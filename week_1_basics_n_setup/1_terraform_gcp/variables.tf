variable "project" {
  description = "Project"
  type        = string
  default     = "data-engineering-zoomcamp-24"
}

variable "location" {
  description = "The location of the resources"
  type        = string
  default     = "EU"
}

variable "region" {
  description = "The region of the resources"
  type        = string
  default     = "europe-west3"
}


variable "kw_dataset_name" {
  description = "The name of the dataset to create"
  type        = string
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "The storage class of the GCS bucket"
  type        = string
  default     = "de-kingsway-terraform-bucket"
}
