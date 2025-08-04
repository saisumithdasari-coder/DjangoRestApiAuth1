Django Oauth App
-
### N-tier architecture
- 2 Python Services
- Wrapped in Docker & Deployed on Google Kubernetes Engine
- Backend written using Django to issue/revoke tokens etc to the frontend service.
- Frontend written in Flask to request and store/use all the token functionality of the backend.
- Used https://django-oauth-toolkit.readthedocs.io/en/latest/ to implement token functionality.

##### Run Locally:
via Docker compose:
```bash
docker-compose up --build
```

via Minikube:
```bash
kubectl apply -f kube/deployment.yaml
```

##### View Web Service at:
- Frontend: http://34.105.239.60:5000/
- Backend: http://34.89.36.19:8000/

#### Enpoints of backend are:
```bash
/register/
/login/
/logout/
/refresh/
/api/hello/
```

They can be accessed as such:
```bash
http post http://34.89.36.19:8000/register/ username='test1' password='password'
http post http://34.89.36.19:8000/login/ username='test1' password='password'
http post http://34.89.36.19:8000/logout/ token='zHBfbaO1NYXCGZjFAwarKtVKom3hxw'
http post http://34.89.36.19:8000/refresh/ refresh_token='kIuQ3enXkoDSS1Q4pEYr7uOgr6snX3'
http http://34.89.36.19:8000/api/hello/ 'Authorization: Bearer XpLAPD7fpViEsknIWR8XyThvlKpIxl'
```

All these endpoints can also be accessed on the frontend. The hello or Super Secret Message on the frontend displays token auth working. Only logged in users with valid tokens can view.

The frontend is meant to output results so you can see the results from the backend and demo only. Obviously wouldn't do this outside of demo.