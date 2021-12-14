terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 2.88"
    }
  }
  backend "azurerm" {
    resource_group_name  = "McLaren1_JoeBawn_ProjectExercise"
    storage_account_name = "jbtodoappterraformstate"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}
provider "azurerm" {
  features {}
}
data "azurerm_resource_group" "main" {
  name = "McLaren1_JoeBawn_ProjectExercise"
}
data "azurerm_cosmosdb_account" "main" {
  name                = "jb-todo-app"
  resource_group_name = data.azurerm_resource_group.main.name
}
data "azurerm_cosmosdb_mongo_database" "main" {
  name                = "mongodb"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = data.azurerm_cosmosdb_account.main.name
}
resource "azurerm_app_service_plan" "main" {
  name                = "terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  kind                = "Linux"
  reserved            = true
  sku {
    tier = "Basic"
    size = "B1"
  }
}
resource "azurerm_app_service" "main" {
  name                = "${var.prefix}-ToDo-App-Mod12"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  app_service_plan_id = azurerm_app_service_plan.main.id
  site_config {
    app_command_line = ""
    linux_fx_version = "DOCKER|joebawn/todo-app:latest"
  }
  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "FLASK_APP"                  = "todo_app/app"
    "MONGO_URL"                  = "mongodb://${data.azurerm_cosmosdb_account.main.name}:${data.azurerm_cosmosdb_account.main.primary_key}@${data.azurerm_cosmosdb_account.main.name}.mongo.cosmos.azure.com:10255/DefaultDatabase?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@${data.azurerm_cosmosdb_account.main.name}@"
    "MONGO_DB_NAME"              = "${data.azurerm_cosmosdb_mongo_database.main.name}"
    "LOGIN_DISABLED"             = "False"
    "CLIENTID"                   = var.CLIENTID
    "CLIENTSECRET"               = var.CLIENTSECRET
    "AUTH_REDIRECT_URL"          = "https://github.com/login/oauth/authorize"
    "AUTH_TOKEN_URL"             = "https://github.com/login/oauth/access_token"
    "AUTH_API_URL"               = "https://api.github.com/user"
    "SECRET_KEY"                 = var.SECRET_KEY
  }
}
