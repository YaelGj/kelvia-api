terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "4.6.0"
    }
  }
}

# Le fournisseur docker pilote le démon Docker du codespace :
# nos « VM » sont des conteneurs (substitut pédagogique d'un vrai cloud).
provider "docker" {}

# Nombre de « VM » web (prolongement du TP 3).
variable "nombre_vm" {
  type    = number
  default = 2
}

# Image des « VM », construite à partir de vm/Dockerfile.
resource "docker_image" "vm" {
  name = "kelvia-vm"
  build {
    context = "${path.module}/vm"
  }
}

# À compléter (TP 3) : le réseau kelvia et les « VM » vm-web-1 et vm-web-2.
