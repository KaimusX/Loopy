import pandas as pd

class Playlist:
    #create the dataframe to hold all of the playlists, this should be run once
    def create_dataframe():
        # Create a DataFrame with each row as a playlist
        df = pd.DataFrame({'PlayList_Name': [], 'ID': [], 'User': [], 'Video1': [], 'Video2': [], 'Video3': [], 'Video4': [], 'Video5': [], 'Video6': [], 'Video7': [], 'Video8': [], 'Video9': [], 'Video10': [], 'Audio1': [], 'Audio2': [], 'Audio3': [], 'Audio4': [], 'Audio5': [], 'Audio6': [], 'Audio7': [], 'Audio8': [], 'Audio9': [], 'Audio10': []})
        # Save the DataFrame to a CSV file
        df.to_csv('playlists.csv', index=False)
    def create_playlist():
        # Load the DataFrame from the CSV file
        df = pd.read_csv('playlists.csv')
        # Get the user's input for the playlist name
        playlist_name = input('Enter the name of the playlist: ')
        # Create a new row for the playlist
        new_row = {'PlayList_Name': playlist_name, 'ID': len(df) + 1, 'User': 'User1', 'Video1': '', 'Video2': '', 'Video3': '', 'Video4': '', 'Video5': '', 'Video6': '', 'Video7': '', 'Video8': '', 'Video9': '', 'Video10': '', 'Audio1': '', 'Audio2': '', 'Audio3': '', 'Audio4': '', 'Audio5': '', 'Audio6': '', 'Audio7': '', 'Audio8': '', 'Audio9': '', 'Audio10': ''}
        # Add the new row to the DataFrame
        df = df._append(new_row, ignore_index=True)
        # Save the updated DataFrame to the CSV file
        df.to_csv('playlists.csv', index=False)
    
def main():
    #this should only be run once
    #Playlist.create_dataframe()
    Playlist.create_playlist()

if __name__ == "__main__":
    main() 

