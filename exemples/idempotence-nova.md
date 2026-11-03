# Preuve d'idempotence — pizzeria Nova (exemple)

## Second `terraform apply`

```text
docker_network.nova: Refreshing state... [id=be8514c77b3eb0f2d8ed527713d08dc7f6088be12d2fec15aa80da49640c858d]
docker_container.web_2: Refreshing state... [id=d7dec42fe8e7d6c926e76ea6422452d76a1a29dcb3ec74a53fe438f05e4c6163]
docker_container.web_1: Refreshing state... [id=e0a1d2508106b407f1cd4fb0fa58f1f26aaa63a2b5dede1afa0a34579b24a9ff]

No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration and found no differences, so no changes are needed.

Apply complete! Resources: 0 added, 0 changed, 0 destroyed.
```

Ce qui prouve l'idempotence : aucune ressource ajoutée, modifiée ni détruite.

## Second `ansible-playbook -i inventaire.yaml site.yaml`

```text
PLAY [web] *********************************************************************

TASK [Gathering Facts] *********************************************************
ok: [vm-web-1]
ok: [vm-web-2]

TASK [Installer nginx] *********************************************************
ok: [vm-web-2]
ok: [vm-web-1]

TASK [Déposer la page d'accueil] ***********************************************
ok: [vm-web-1]
ok: [vm-web-2]

PLAY RECAP *********************************************************************
vm-web-1                   : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
vm-web-2                   : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

Ce qui prouve l'idempotence : dans le PLAY RECAP, `changed=0` pour chaque machine.
