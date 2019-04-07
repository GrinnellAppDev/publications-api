FROM node:8.9

COPY . /app
WORKDIR /app
RUN yarn install

ENV NODE_ENV=production

EXPOSE 80

# Allow node to bind to port 80
RUN setcap cap_net_bind_service=+ep $(readlink -f $(which node))

# Switch to unprivileged user
USER node

CMD ["node", "index.js"]
