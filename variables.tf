variable "prefix" {
  description = "The prefix used for all resources in this environment"
}
variable "location" {
  description = "The Azure location where all resources in this deployment should be created"
  default     = "uksouth"
}
variable "SECRET_KEY" {
  description = "App Secret"
  sensitive   = true
}
variable "CLIENTID" {
  description = "Github OAuth ClientID"
  sensitive   = true
}
variable "CLIENTSECRET" {
  description = "Github OAuth Secret"
  sensitive   = true
}
