import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

# Define the paths for schema and database files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Path to database folder
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")     # Path to schema.sql file
DB_PATH = os.path.join(BASE_DIR, "music_tracker.db")   # Path to SQLite database

# Define the base class for declarative models
Base = declarative_base()

# Define the Video model that corresponds to the "videos" table in the database
class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String, nullable=False)
    name = Column(String)
    artist = Column(String)
    title = Column(String)
    category = Column(String)
    chord = Column(String)
    status = Column(String, default="unread")  # Add default status column

    def __repr__(self):
        return f"<Video(id={self.id}, name={self.name}, artist={self.artist}, status={self.status})>"

class Database:
    def __init__(self, db_url='sqlite:///music_tracker.db'):
        """Initialize the database and ensure schema is applied."""
        # Create an SQLite database engine
        self.engine = create_engine(db_url, echo=True)
        # Create tables in the database
        Base.metadata.create_all(self.engine)
        # Create a session maker to interact with the database
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def initialize_database(self):
        """Read the schema.sql file and initialize the database."""
        try:
            if os.path.exists(SCHEMA_PATH):
                with open(SCHEMA_PATH, "r") as schema_file:
                    schema_sql = schema_file.read()
                # Execute the schema SQL script
                with self.engine.begin() as connection:
                    for statement in schema_sql.split(";"):
                        if statement.strip():
                            connection.execute(text(statement.strip()))  # Use `text` for raw SQL
                print("Database initialized successfully.")
            else:
                print(f"Schema file not found at {SCHEMA_PATH}. Please ensure it exists.")
        except Exception as e:
            print(f"Error initializing the database: {e}")

    def add_video(self, file_name, metadata):
        """Insert a new video record."""
        try:
            new_video = Video(
                file_name=file_name,
                name=metadata["name"],
                artist=metadata["artist"],
                title=metadata["title"],
                category=metadata["category"],
                chord=metadata["chord"]
            )
            self.session.add(new_video)
            self.session.commit()
            print(f"Video '{file_name}' added successfully.")
        except Exception as e:
            print(f"Error adding video: {e}")

    def get_all_videos(self):
        """Retrieve all video records."""
        try:
            return self.session.query(Video).all()
        except Exception as e:
            print(f"Error fetching videos: {e}")
            return None

    def fetch_videos_by_category(self, selected_category):
        """Fetch videos by category from the database."""
        try:
            if selected_category == "All" or not selected_category:
                return self.session.query(Video).all()  # Fetch all videos if "All" is selected
            return self.session.query(Video).filter(Video.category == selected_category).all()  # Filter by category
        except Exception as e:
            print(f"Error fetching videos by category: {e}")
            return None

    def update_video(self, video_id, updated_metadata):
        """Update an existing video record."""
        try:
            video = self.session.query(Video).filter_by(id=video_id).first()
            if video:
                video.name = updated_metadata["name"]
                video.artist = updated_metadata["artist"]
                video.title = updated_metadata["title"]
                video.category = updated_metadata["category"]
                video.chord = updated_metadata["chord"]
                self.session.commit()
                print(f"Video with ID {video_id} updated successfully.")
            else:
                print(f"Video with ID {video_id} not found.")
        except Exception as e:
            print(f"Error updating video: {e}")

    def delete_video(self, video_id):
        """Delete a video record."""
        try:
            video = self.session.query(Video).filter_by(id=video_id).first()
            if video:
                self.session.delete(video)
                self.session.commit()
                print(f"Video with ID {video_id} deleted successfully.")
            else:
                print(f"Video with ID {video_id} not found.")
        except Exception as e:
            print(f"Error deleting video: {e}")

    def close(self):
        """Close the database session."""
        if self.session:
            self.session.close()
            print("Database session closed.")

    def fetch_videos(self, selected_category="All"):
        """Fetch videos and filter them by category if necessary."""
        session = self.Session()
        if selected_category == "All" or not selected_category:
            videos = session.query(Video).all()  # Fetch all videos if "All" is selected
        else:
            videos = session.query(Video).filter(Video.category == selected_category).all()  # Filter by category
        session.close()
        return videos

    def get_video_by_filename(self, filename):
        """Fetch a video record by its filename."""
        try:
            video = self.session.query(Video).filter_by(file_name=filename).first()
            return video
        except Exception as e:
            print(f"Error fetching video by filename: {e}")
            return None

    def update_video_status(self, filename, status):
        """Update the status of a video (e.g., read/unread)."""
        try:
            video = self.get_video_by_filename(filename)
            if video:
                video.status = status  # Update the status field
                self.session.commit()   # Commit the changes to the database
                print(f"Video '{filename}' status updated to {status}.")
            else:
                print(f"Video with filename '{filename}' not found.")
        except Exception as e:
            print(f"Error updating video status: {e}")
