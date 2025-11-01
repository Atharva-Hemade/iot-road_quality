# Use Nginx to serve static files
FROM nginx:alpine

# Remove default Nginx static files
RUN rm -rf /usr/share/nginx/html/*

# Copy your HTML into the Nginx folder
COPY index.html /usr/share/nginx/html/

# Expose Nginx default port
EXPOSE 80

# Run Nginx automatically
CMD ["nginx", "-g", "daemon off;"]