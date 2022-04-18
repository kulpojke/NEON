FROM mambaorg/micromamba:0.22.0

COPY --chown=$MAMBA_USER:$MAMBA_USER geo3.yaml /tmp/env.yaml

RUN micromamba install -y -f /tmp/env.yaml && \
    micromamba clean --all --yes