FROM node:8.9

COPY . /app
WORKDIR /app
RUN yarn install

ENV NODE_ENV=production

EXPOSE 80

CMD ["node", "index.js"]
