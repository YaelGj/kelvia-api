# Preuve d'idempotence — pizzeria Nova (exemple)

## Second `terraform apply`

```text
docker_network.nova: Refreshing state... [id=186fc5e09766a8ef422adc0adeff8b20a19b120acba8a903f0107ba67d268c66]
docker_image.vm: Refreshing state... [id=sha256:474562ae4692c866b6df522c34dee0e87c3abb83ed59ce707e78563b2a6062cbnova-vm]
docker_container.web_1: Refreshing state... [id=3fc247f4a197a0ccc6540e2e4cefc1c48bd41c6435234e6eaa0e5e29b0f28588]
docker_container.web_2: Refreshing state... [id=8710addcde84ae040b598bf0882deef427742600111d2f2502a5bf12de662557]

No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration and found no differences, so no changes are needed.

Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
```

Ce qui prouve l'idempotence : aucune ressource ajoutée, modifiée ni détruite.

## Second `ansible-playbook -i inventaire.yaml site.yaml`

```text

PLAY [all] *********************************************************************

TASK [Gathering Facts] *********************************************************
ok: [vm-web-1]
ok: [vm-web-2]

TASK [Configurer la vitrine] ***************************************************
ok: [vm-web-1]
ok: [vm-web-2]

PLAY RECAP *********************************************************************
vm-web-1                   : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
vm-web-2                   : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

Ce qui prouve l'idempotence : dans le PLAY RECAP, `changed=0` pour chaque machine.
