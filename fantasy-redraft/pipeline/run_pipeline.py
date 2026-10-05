from ingestion.sample_ingest import save_raw_data
from transformations.normalize_players import main as normalize_players
from transformations.score_players import main as score_players
from pipeline.upload_to_s3 import upload_file

def run_pipeline():
    print("Starting fantasy football data pipeline...")

    try:
        print("Step 1: Ingesting raw data...")

        sample_data = {
            "source": "sample",
            "players": [
                {
                    "name": "Test QB",
                    "position": "QB",
                    "pass_yd": 300,
                    "pass_td": 3,
                    "interception": 1
                },
                {
                    "name": "Test RB",
                    "position": "RB",
                    "rush_yd": 110,
                    "rush_td": 1,
                    "receptions": 4
                }
            ]
        }

        save_raw_data(sample_data, "sample_players.json")
        print("Step 1 complete.")

        print("Step 2: Normalizing player data...")
        normalize_players()
        print("Step 2 complete.")

        print("Step 3: Scoring players...")
        score_players()
        print("Step 3 complete.")

        print("Step 4: Uploading scored data to s3")
        upload_file()

        print("Pipeline completed successfully.")

    except Exception as error:
        print(f"Pipeline failed: {error}")
        raise


if __name__ == "__main__":
    run_pipeline()