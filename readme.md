# AutoLogin

構建鏡像
```
docker build -t ef -f app/dockerfile . --no-cache
docker push ef
```

編輯ENV
```
cp .local.env .env
```

啟動服務
```
docker-compose up
```

