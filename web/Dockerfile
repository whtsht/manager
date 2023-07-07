FROM node:latest

WORKDIR /app

COPY ./web/ /app

RUN mkdir -p node_modules \
    && chown node node_modules

RUN yarn \
    && yarn build


FROM nginx:latest

RUN mkdir -p /etc/nginx/ssl \
    && mkdir -p /var/www/guide_me/html

COPY ./web/nginx.conf /etc/nginx/nginx.conf
COPY ./secret/ssl/nginx.pem /etc/nginx/ssl/nginx.pem
COPY ./secret/ssl/nginx.key /etc/nginx/ssl/nginx.key

COPY --from=0 /app/build /var/www/guide_me/html 

CMD ["nginx", "-g", "daemon off;"]
