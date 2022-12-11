
FROM nginx:1.15.9-alpine

ADD ./docker_cfg/nginx/conf/ /etc/nginx/conf.d/
ADD ./docker_cfg/nginx/proxy_params /etc/nginx/proxy_params

CMD ["nginx", "-g", "daemon off;"]