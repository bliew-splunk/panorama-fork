#!/usr/bin/env bash
if [ -z "$1" ]
  then
    echo "Run this from outside the repo directory's parent."
    echo "Usage: $0 <repo_dir_name>"
    exit 1
fi
repo_name=$(basename "$1")
version=$(cat "$repo_name/panorama.json" | jq --raw-output ".app_version")
echo "repo_name=$repo_name, version=$version"
output_name="${repo_name}-${version}.tgz"
echo "Writing to $output_name"
tar --exclude=".*" -zcf "$output_name" panorama-fork