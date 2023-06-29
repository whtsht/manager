FROM nginx:latest

RUN mkdir -p /etc/nginx/ssl

COPY ./proxy/nginx.conf /etc/nginx/nginx.conf
COPY ./secret/ssl/nginx.pem /etc/nginx/ssl/nginx.pem
COPY ./secret/ssl/nginx.key /etc/nginx/ssl/nginx.key

CMD ["nginx", "-g", "daemon off;"]
