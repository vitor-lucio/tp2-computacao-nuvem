#teste argocd
wget --server-response \
    --output-document response.out \
    --header='Content-Type: application/json' \
    --post-data '{"songs": ["Black Beatles", "Bounce Back"]}'\
    http://10.109.126.114:32216/api/recommender