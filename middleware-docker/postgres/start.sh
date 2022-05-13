docker run --network=host -d --rm --name postgres -e POSTGRES_PASSWORD=postgres -v /data/kefeng/postgres/data:/var/lib/postgresql/data postgres:latest
