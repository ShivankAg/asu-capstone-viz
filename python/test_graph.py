import pandas as pd
import matplotlib.pyplot as plt

def process_data(data, iteration):
    # Placeholder function to process the received data
    # You can customize this function based on your actual processing requirements
    print("Processing data:", data)

    # Update the scatter plot with the new altitude data
    altitude = data['Altitude']
    plt.scatter(iteration, altitude, color='blue')
    plt.legend()
    plt.savefig('live_plot.png')  # Save the plot as an image file
    plt.pause(0.1)  # Pause to update the graph

def simulate_data_processing(file_path):
    iteration = 0
    while True:
        try:
            # Load the CSV file into a DataFrame
            df = pd.read_csv(file_path)
            
            # Process the data
            for index, row in df.iterrows():
                process_data(row, iteration)
                iteration += 1
            
            # Sleep for 10 seconds before processing the next batch
            plt.pause(10)
            
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    # Replace 'ParsedSpaceDucksData.csv' with the actual path to your CSV file
    file_path = 'ParsedSpaceDucksData.csv'
    
    # Set up the initial scatter plot
    plt.scatter([], [], label='Altitude', color='blue')
    plt.legend()
    plt.savefig('live_plot.png')  # Save the initial plot as an image file
    plt.show()

    # Run the simulation
    simulate_data_processing(file_path)
