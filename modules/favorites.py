import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import text

# Define the paths for schema and database files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Path to database folder
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

# Define the Favorites model that stores favorite videos (using a relation to the Video model)
class Favorite(Base):
    __tablename__ = 'favorites'

    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(Integer, ForeignKey('videos.id', ondelete="CASCADE"))
    video = relationship("Video", backref="favorites")  # Create relationship with Video table

    def __repr__(self):
        return f"<Favorite(id={self.id}, video_id={self.video_id})>"

class FavoritesDatabase:
    def __init__(self, db_url='sqlite:///music_tracker.db'):
        """Initialize the database and ensure schema is applied."""
        self.engine = create_engine(db_url, echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def add_to_favorites(self, video_id):
        """Add a video to the favorites table."""
        try:
            favorite = Favorite(video_id=video_id)
            self.session.add(favorite)
            self.session.commit()
            print(f"Video with ID {video_id} added to favorites.")
        except Exception as e:
            print(f"Error adding video to favorites: {e}")

    def remove_from_favorites(self, video_id):
        """Remove a video from the favorites table."""
        try:
            favorite = self.session.query(Favorite).filter_by(video_id=video_id).first()
            if favorite:
                self.session.delete(favorite)
                self.session.commit()
                print(f"Video with ID {video_id} removed from favorites.")
            else:
                print(f"Video with ID {video_id} not found in favorites.")
        except Exception as e:
            print(f"Error removing video from favorites: {e}")

    def get_favorite_videos(self):
        """Retrieve all favorite videos."""
        try:
            favorites = self.session.query(Favorite).all()
            favorite_videos = [favorite.video for favorite in favorites]
            return favorite_videos
        except Exception as e:
            print(f"Error fetching favorite videos: {e}")
            return []

    def close(self):
        """Close the database session."""
        if self.session:
            self.session.close()
            print("Favorites database session closed.")

# Example Usage
if __name__ == "__main__":
    db = FavoritesDatabase()

    # Fetching all favorite videos
    all_favorites = db.get_favorite_videos()
    print("Favorite Videos:", all_favorites)

    db.close()
