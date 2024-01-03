terraform {
  required_version = ">= 0.12"


required_providers {
    docker = {
      source = "kreuzwerker/docker"
      version = "2.15.0" # Specify the version you want to use
    }
  }
}
provider "docker" {
    host = "tcp://127.0.0.1:2375"
}


resource "docker_container" "firewall" {
  name  = "firewall"
  
  # Set the image attribute based on your service configuration
  image = "alessandrablasioli/my_firewall_image:latest"  # Set the image dynamically

  # Altre configurazioni per il servizio firewall
  
  # Se il servizio espone le porte, aggiungi questa configurazione
  
}

resource "docker_container" "client" {
  name  = "client"
  
  # Set the image attribute based on your service configuration
  image = "alessandrablasioli/my_client_image:latest"  # Set the image dynamically

  # Altre configurazioni per il servizio client
  
  # Se il servizio espone le porte, aggiungi questa configurazione
  
}

resource "docker_container" "client-2" {
  name  = "client-2"
  
  # Set the image attribute based on your service configuration
  image = "alessandrablasioli/my_client_image:latest"  # Set the image dynamically

  # Altre configurazioni per il servizio client-2
  
  # Se il servizio espone le porte, aggiungi questa configurazione
  
}

resource "docker_container" "database" {
  name  = "database"
  
  # Set the image attribute based on your service configuration
  image = "alessandrablasioli/my_database_image:latest"  # Set the image dynamically

  # Altre configurazioni per il servizio database
  
  # Se il servizio espone le porte, aggiungi questa configurazione
  
}

resource "docker_container" "webserver" {
  name  = "webserver"
  
  # Set the image attribute based on your service configuration
  image = "alessandrablasioli/my_webserver_image:latest"  # Set the image dynamically

  # Altre configurazioni per il servizio webserver
  
  # Se il servizio espone le porte, aggiungi questa configurazione
  
  ports {
    
    internal = 8080  # Porta interna del servizio Docker
    external = 80  # Porta esterna del servizio
    
  }
  
}

resource "docker_container" "server" {
  name  = "server"
  
  # Set the image attribute based on your service configuration
  image = "alessandrablasioli/my_server_image:latest"  # Set the image dynamically

  # Altre configurazioni per il servizio server
  
  # Se il servizio espone le porte, aggiungi questa configurazione
  
}
