cat frhd5490/files.csv | xargs -P 10 -d '\n' -I {} sh -c '
  filename=$(echo "{}" | cut -d, -f1)
  url=$(echo "{}" | cut -d, -f2)
  wget -c "$url" -O "source-store/frhd5490/$filename"
'