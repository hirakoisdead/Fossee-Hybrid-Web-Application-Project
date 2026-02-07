# Build stage
FROM node:18-alpine AS build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build argument for API URL
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy custom nginx config template
COPY nginx.conf /etc/nginx/templates/default.conf.template

# Copy built files from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Railway requires listening on PORT env var
ENV PORT=80

# Expose port
EXPOSE 80

# Use envsubst to replace PORT and start nginx
CMD sh -c "envsubst '\$PORT' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"

