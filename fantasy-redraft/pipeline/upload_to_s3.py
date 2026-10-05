#local file is scored_players, which gets uploaded to our bucket name, and stored as our s3 key
#boto3 is python package. can be fit into docker.
import boto3

BUCKET_NAME = "fantasy-pipeline-momandpopshop"
LOCAL_FILE = "data/processed/scored_players.json"                   #the file we wanna upload, with our scored players
S3_KEY = "processed/scored_players.json"                               #where file will be inside bucket. store this object under this name


def upload_file():
    s3 = boto3.client("s3")                                         #creates python connection to AWS s3

    s3.upload_file(
        LOCAL_FILE,
        BUCKET_NAME,
        S3_KEY                                                         #key is literally just name/address of object inside bucket
    )                                                               #source file, destination bucket, destination key

    print(f"Uploaded {LOCAL_FILE} to s3://{BUCKET_NAME}/{S3_KEY}")

if __name__ == "__main__":
    upload_file()
