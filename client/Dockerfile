FROM node:10.15.0-alpine
RUN apk add --no-cache bash
WORKDIR /client
#VOLUME ["/client"]
COPY package*.json ./
RUN npm install
EXPOSE 8080
CMD ["npm", "run", "serve"]