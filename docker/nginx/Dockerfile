FROM nginx

# Remove default nginx config
USER root

# Ensure parent directories exist and create static and media directories
RUN rm /etc/nginx/conf.d/default.conf \
    && mkdir -p /var/html/www/mediplant/static \
    && mkdir -p /var/html/www/mediplant/media \
    && chmod 777 -R /var/html/www/mediplant/media \
    && chmod 777 -R /var/html/www/mediplant/static

# Copy custom nginx config
COPY ./backend.conf /etc/nginx/conf.d/

# Expose ports
EXPOSE 80 443

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
