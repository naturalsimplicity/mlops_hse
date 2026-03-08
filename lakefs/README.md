## LakeFS

Запуск

```shell
docker compose up -d db
docker compose up -d minio
docker compose up -d lakefs
docker compose ps
docker compose logs --tail=200 lakefs
```

Использование

```shell
lakectl repo list
lakectl repo create lakefs://firstproj s3://lakefs-artifacts/firstproj --default-branch main
lakectl branch create lakefs://firstproj/featone --source main

mkdir -p workdir && cd workdir
echo "hello from featone v1" > note.txt

lakectl fs upload note.txt lakefs://firstproj/featone/note.txt
lakectl commit lakefs://firstproj/featone -m "Add/update note.txt in featone"
lakectl merge lakefs://firstproj/featone lakefs://firstproj/main -m "Merge featone into main"
```
