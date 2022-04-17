# xontex-api
this is the backend api, using :
- FastApi
- MongoDB
- Pydantic

### Example .env
```
MONGODB_AUTH="mongodb://USERNAME:PASSWORD@IP/xontex"
APP_USERNAME="YOURUSERNAME"
APP_PASSWORD="YOURPASSWORD"
```

### submitJawaban Schema
```
"data": {
  "soal": "PHA+IERpYmF3YWggaW5pIG1lcnVwYWthbiBjb250b2ggL3QgL24gPC9wPg==",
  "jawaban": "PGxhYmVsPiAxMjAvNDAgPSAzIDwvbGFiZWw+",
  "username": "bunga",
}
```

### onloadGetJawaban Schema
```
"data": {
    "soal": "PHA+IERpYmF3YWggaW5pIG1lcnVwYWthbiBjb250b2ggL3QgL24gPC9wPg==",
    "jawab": [
      {
      "username": "bunga", 
      "jawaban": "PGxhYmVsPiAxMjAvNDAgPSAzIDwvbGFiZWw+"
      }
    ],
  }
}
```

### errors on onloadGetJawaban schema 
```
"data": {
  "jawab": [
      {
        "username": "Belum ada jawaban", 
        "jawaban": " "
      }
    ]
  },
```
