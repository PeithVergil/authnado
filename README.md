Testing the `authorize` endpoint. 

Authorization Code Grant

```bash
http://127.0.0.1:8080/v1/auth?client_id=hello&client_secret=world&response_type=code
```

Implicit Grant

```bash
http://127.0.0.1:8080/v1/auth?client_id=hello&client_secret=world&response_type=token
```

Testing the `tokens` endpoint.

```bash
http -v http://127.0.0.1:8080/v1/auth/tokens client_id=hello client_secret=world grant_type=client_credentials
```

```bash
http -v http://127.0.0.1:8080/v1/auth/tokens "grant_type=authorization_code" "code=T5Bd8Y7acxtyFhPGJY7lSODHYNWawO"
```