docker build -t webapp .
docker run --rm --name nginx -p 8080:80 -it webapp

W celu uruchomienia dockera należy skorzystać z powyższych komend.