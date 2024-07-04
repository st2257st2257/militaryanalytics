# NODE
FROM alpine:3.18 as node_inst


RUN  apk update \
  && apk upgrade \
  && apk add --update nodejs npm \
  && rm -rf /var/cache/apk/*



# BUILD
FROM node_inst AS build

WORKDIR /build

COPY ./package* .
RUN npm i

ARG VITE_BACKEND_URL
COPY . .
RUN npm run build



# RUN
FROM alpine:3.18

RUN apk update && \
    apk add --no-cache nginx nginx-mod-http-headers-more

EXPOSE 8080

WORKDIR /usr/share/nginx/html/

COPY --from=build /build/dist /usr/share/nginx/html/

# Launch as non-sudo user
RUN chown -R 1001:0 /var/lib/nginx /var/log/nginx /var/run/ && \
    chmod -R g=u /var/lib/nginx /var/log/nginx /var/run/

USER 1001

CMD ["nginx", "-g", "daemon off;"]
