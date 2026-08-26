import boto3

s3 = boto3.client("s3")
response = s3.list_buckets()

buckets = response["Buckets"]
print(f"Found {len(buckets)} buckets")

for bucket in buckets:
    name = bucket["Name"]
    try:
        pab = s3.get_public_access_block(Bucket=name)
        config = pab["PublicAccessBlockConfiguration"]
        if all(config.values()):
            print(f"OK: {name} - public access fully blocked")
        else:
            print(f"WARNING: {name} - public access NOT fully blocked")
    except s3.exceptions.ClientError:
        print(f"RISK: {name} - NO public access block configured")
