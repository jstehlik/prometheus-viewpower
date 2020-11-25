FROM alpine:3.12

ARG CREATED
ARG VERSION
ARG REVISION

LABEL org.opencontainers.image.created="$CREATED"
LABEL org.opencontainers.image.url="https://github.com/jstehlik/prometheus-viewpower"
LABEL org.opencontainers.image.source="https://github.com/jstehlik/prometheus-viewpower"
LABEL org.opencontainers.image.version="$VERSION"
LABEL org.opencontainers.image.revision="$REVISION"
LABEL org.opencontainers.image.vendor="Josef Stehlik <josef@stehlik.sh>"
LABEL org.opencontainers.image.title="prometheus-viewpower"
LABEL org.opencontainers.image.description="Prometheus metrics provider for ViewPower UPS software"
LABEL org.opencontainers.image.authors="Josef Stehlik <josef@stehlik.sh>"
LABEL org.opencontainers.image.licenses="MIT"

RUN apk add --no-cache python3 shadow su-exec
ENV UID=1000 GID=1000 FLASK_APP=prometheusviewpower:create_app PROMETHEUS_VIEWPOWER_CONFIGFILE=/config.json PATH="/app/.venv/bin:$PATH"
RUN addgroup -S -g $GID prometheusviewpower && adduser -S prometheusviewpower -u $UID -G prometheusviewpower

COPY --chown=prometheusviewpower:prometheusviewpower prometheus_viewpower /app/prometheus_viewpower
WORKDIR /app
RUN python3 -m venv /app/.venv
COPY requirements.txt docker-entrypoint.sh ./
RUN pip3 install -r requirements.txt
RUN chmod +x docker-entrypoint.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]

EXPOSE 5600
CMD ["prometheusviewpower"]