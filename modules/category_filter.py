def filter_videos_by_category(videos, selected_category):
    """Filter videos based on the selected category."""
    if selected_category == "All" or not selected_category:
        return videos  # If "All" or no category selected, return all videos
    
    # Filter videos based on category (assuming the category is at index 5 in the database)
    filtered_videos = [video for video in videos if video[5] == selected_category]  # 5 is the index for category
    
    return filtered_videos
