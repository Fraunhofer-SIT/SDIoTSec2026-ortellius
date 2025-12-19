#!/bin/bash

set -e

mkdir cache
mkdir cache/svds
pushd cache/svds
    ## 1) from cmsis-svd

    git clone --recurse-submodules https://github.com/cmsis-svd/cmsis-svd-data

    ## 2) from Keil

    git clone https://gist.github.com/f680895a3bdd412d760a2e37a2f65365.git keil
    pushd keil
        git apply <<'EOF'
diff --git a/download_keil_svd.py b/download_keil_svd.py
index 1508fec..b8c95ec 100644
--- a/download_keil_svd.py
+++ b/download_keil_svd.py
@@ -13,7 +13,9 @@ import re
 import zipfile
 from io import BytesIO

-import requests
+# requests library sometimes has trouble with DNS in CI environments
+from requests_doh import DNSOverHTTPSSession
+requests = DNSOverHTTPSSession()

 # Some websites are blocking requests based on User-Agent header
 USER_AGENT = (
EOF
        python3 download_keil_svd.py
        python3 download_keil_svd.py
        python3 download_keil_svd.py
    popd

    ## finalize

    mkdir data
    mv cmsis-svd-data/data/ data/cmsis
    mv keil/keil-svd data/keil

    find data -type f -not \( -name "*.svd" -o -name "*.xml" \) -delete
    find data -type d -empty -delete
popd

rm -rf svds
mv cache/svds/data svds
find svds -type f -exec chmod -x {} +

tar czvf svds.tar.gz svds
