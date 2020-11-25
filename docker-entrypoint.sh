#!/bin/sh
if [[ "$1" = "prometheusviewpower" && "$(id -u)" = "0" ]]; then
  echo "Setting $UID for user prometheusviewpower"
  usermod -u $UID prometheusviewpower
  echo "Setting $GID for group prometheusviewpower"
  groupmod -g $GID prometheusviewpower
  cd /app
  su-exec prometheusviewpower:prometheusviewpower gunicorn -b :5600 --access-logfile - 'prometheus_viewpower:create_app()'
fi
