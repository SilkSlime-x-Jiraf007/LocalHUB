FROM node:19-alpine3.15
COPY package.json /app/package.json
COPY package-lock.json /app/package-lock.json
WORKDIR /app
RUN npm install

COPY vite.config.js /app/vite.config.js
COPY index.html /app/index.html
COPY public /app/public
COPY src /app/src
CMD ["npm", "run", "dev", "--", "--host"]