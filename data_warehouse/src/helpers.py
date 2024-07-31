import pandas as pd
from numpy import NaN
import uuid

def generate_uuid():
    return str(uuid.uuid4().hex[:8].upper())

# function to extract performer details
def extract_performers(movies_excel_df):
    data = []

    for index, row in movies_excel_df.iterrows():
        movie_index_ref = index + 1
        movie_title = row['name']
        performers = row['performers']

        # Split the performers by commas and extract names and roles
        performers_list = performers.split('-')
        for performer in performers_list:
            name_role = performer.strip().split('(')
            performer_name = name_role[0].strip()
            performer_role = name_role[1].replace(')', '').strip() if len(name_role) > 1 else None

            # Append the data to the list
            data.append({
                'id': movie_index_ref,
                'movieTitle': movie_title,
                'performerName': performer_name,
                'performerRole': performer_role
            })

    # Create a new DataFrame from the extracted data
    performers_df = pd.DataFrame(data)
    return performers_df


def assign_score(quartile, median, value):
  if value >= quartile:
    return 100
  elif value >= median and value < quartile:
    return 80
  elif value>=1 and value < median:
    return 70
  else:
    return NaN


# Prepare dimScore DataFrame
def generate_comment(score):
	movieComment = "excelent movie. One of my favourites. Highly recommended"
	if pd.isna(score):
		movieComment = ""
	elif score>=80:
		movieComment = "very nice movie. I recommend it"
	elif score>=70 and score<80:
		movieComment = "good movie. Enjoyable"
	elif score>=60 and score<70:
		movieComment = "good to spend some time if there isn't anything else. Could be better"
	elif score>=50 and score<60:
		movieComment = "just another movie. Personally I didnt like it. Up to you to watch it"
	else:
		movieComment = "Awful. don't waste your time"

	return movieComment


# Function to generate interaction data
def generate_interaction_data(row):
    finish_count = 1
    play_count = 1
    back_click_count = 0
    movie_forward_count = 0
    movie_view_percentage = 100.00

    return {
        'username':row['name'],
        'finishCount': finish_count,
        'backClickCount': back_click_count,
        'movieForwardCount': movie_forward_count,
        'playCount': play_count,
        'movieViewPercentage': movie_view_percentage
    }
