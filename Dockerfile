FROM nginx:alpine
# Add this line to upgrade existing packages to their fixed versions
RUN apk update && apk upgrade --no-cache
COPY target/pipeline8/*.html /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf
