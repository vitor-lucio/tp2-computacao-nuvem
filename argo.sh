argocd app create guestbook \
      --repo https://github.com/vitor-lucio/tp2-computacao-nuvem.git \
      --path Kubernetes \
      --project matheussilva-project \
      --dest-namespace matheussilva \
      --dest-server https://kubernetes.default.svc \
      --sync-policy auto
