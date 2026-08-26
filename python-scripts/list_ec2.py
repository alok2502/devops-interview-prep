import boto3

ec2 = boto3.client("ec2")
response = ec2.describe_instances()
stopped = 0

def get_names(instance):
    tags = instance.get("Tags", [])
    for tag in tags:
        if tag["Key"] == "Name":
            return tag["Value"]
    return "No Name"
    

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        instance_id = instance["InstanceId"]
        state = instance["State"]["Name"]
        instance_type = instance["InstanceType"]
        instance_name = get_names(instance)
        # print(f"{instance_id} | {state} | {instance_type}")

        if state == "stopped":
            print(f"Stopped Instanace : {instance_name} ({instance_id} - {instance_type})")
            stopped += 1
print(f"Total Stopped Instances are : {stopped}")

