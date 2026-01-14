
    FROM node:18-alpine AS builder

    WORKDIR /app

    COPY package.json package-lock.json ./
    

    RUN npm install --production=false
    
    COPY . .
    
   
    RUN npx next build
    

    FROM node:18-alpine
    
    WORKDIR /app
    
    COPY package.json ./
    RUN npm install --production
    
    COPY --from=builder /app/.next /app/.next
    
    COPY --from=builder /app/public /app/public
    COPY --from=builder /app/package.json /app/package.json
    COPY --from=builder /app/next.config.js /app/next.config.js
    
    EXPOSE 3000
    
    CMD ["npm", "start"]