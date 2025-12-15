# ------------------------------------------------------------------
# 1. BUILD STAGE: Generates the static files and server bundle
# ------------------------------------------------------------------
    FROM node:18-alpine AS builder

    # Set working directory inside the container
    WORKDIR /app
    
    # Copy dependency files only for caching. This is critical for fast rebuilds.
    # If these files haven't changed, the 'npm install' step is cached.
    COPY package.json package-lock.json ./
    
    # Install dependencies (This creates the node_modules folder inside the container)
    # We use --production=false to ensure dev dependencies (like typescript, next, etc.) 
    # needed for the build are installed.
    RUN npm install --production=false
    
    # Copy all source code
    COPY . .
    
    # Build the Next.js application bundle
    # FIX: The error message indicates the underlying 'npm run build' command is still tied 
    # to the old 'remix build' command in package.json. We explicitly call the Next.js 
    # binary using npx to ensure the correct build process is executed, even before 
    # the user updates their package.json file.
    RUN npx next build
    
    
    # ------------------------------------------------------------------
    # 2. RUN STAGE: Creates the final, minimal production server image
    # ------------------------------------------------------------------
    # Use a smaller base image for production
    FROM node:18-alpine
    
    # Set working directory
    WORKDIR /app
    
    # Only install production dependencies. This significantly reduces the final image size.
    COPY package.json ./
    RUN npm install --production
    
    # 1. Copy the built artifacts from the builder stage
    # The '.next' folder contains all compiled Next.js assets, server files, and build info.
    COPY --from=builder /app/.next /app/.next
    
    # 2. Copy static assets and the package.json for the 'start' script
    COPY --from=builder /app/public /app/public
    COPY --from=builder /app/package.json /app/package.json
    COPY --from=builder /app/next.config.js /app/next.config.js
    
    # Expose the default port for Next.js production server
    EXPOSE 3000
    
    # Command to run the Next.js production server (assumes "start": "next start" in package.json)
    CMD ["npm", "start"]