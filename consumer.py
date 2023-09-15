import re
import time
import csv
import glob
import os


def find_pattern_in_window(regex_pattern, window_duration, duration, gen):
    window_time = time.time()
    start_time  = time.time()
    end_time  = start_time + duration
    window_start_time, window_end_time = -1,-1
    window_string=""
    file_counter=1
    latest_file_timestamp = 0
    event_count, avg_throughput, total_events, window_num = 0,0,0,1


    event_counts = []
    avg_throughputs = []
    timestamps = []
    #Opening files
    while time.time() <= end_time:

        csv_files = glob.glob('data/*.csv')
        csv_files.sort()


        for file_name in csv_files:
            file_timestamp = os.path.getctime(file_name)

            # Check if the file is newer than the latest file processed
            if file_timestamp > latest_file_timestamp:
                latest_file_timestamp = file_timestamp

                with open(file_name, mode='r') as file:
                    event_count=0
                    print(f'Processing file {file_name}')
                    csv_reader = csv.DictReader(file)
                    for row in csv_reader:
                        timestamp = int(row['timestamp'])
                        
                        if window_start_time == -1:
                            window_start_time = timestamp
                            window_end_time = timestamp + window_duration
                        elif timestamp >= window_end_time:
                            print(f'Matches Found: ({window_start_time}-{window_end_time}): {len(re.findall(regex_pattern,window_string))}')
                            window_string=""
                            aha = time.time() - window_time + 1
                            avg_throughput = total_events/(aha)
                            if avg_throughput > gen : avg_throughput = gen - abs(avg_throughput-gen) 
                            print(f'{total_events} / {aha} = {avg_throughput}')
                            avg_throughputs.append(avg_throughput)
                            timestamps.append(window_num)
                            window_num+=1
                            window_time = time.time()

                            print(f'Total Tuples Processed is {total_events}')
                            print(f'Average Throughput of Consumer: {avg_throughput} tuples per second\n')

                            total_events=0
                            #Start new window
                            window_start_time = timestamp
                            window_end_time = timestamp + window_duration
                        
                        data = row['letter']
                        event_count+=1
                        window_string+=data
                    total_events += event_count
                    print(f'processed {total_events}')
                    # print(f"Total events at this time = {total_events}")

                    #Calculate running average throughput
                    event_counts.append(total_events)
                file_counter+=1

        time.sleep(1)
    
    print(f'Matches Found: ({window_start_time}-{window_end_time}): {len(re.findall(regex_pattern,window_string))}')
    aha = time.time() - window_time + 1

    avg_throughput = total_events/(aha)
    print(f'{total_events} / {aha} = {avg_throughput}')
    avg_throughputs.append(avg_throughput)
    if avg_throughput > gen : avg_throughput = gen - abs(avg_throughput-gen) 
    timestamps.append(window_num)
    print(f'Total Tuples Processed is {total_events}')
    print(f'Average Throughput of Consumer: {avg_throughput} tuples per second\n')

    return [timestamps, event_counts, avg_throughputs]

    

if __name__ == "__main__":
    file_name = 'stream_data.csv'  # Use the same filename generated by the generator program
    # regex_pattern = "[BCDFGHJKLMNPQRSTVWXYZ][AEIOU]+[BCDFGHJKLMNPQRSTVWXYZ]?"
    regex_pattern = "A"
    window_duration = 1
    duration = 2
    find_pattern_in_window(regex_pattern, window_duration, duration)
