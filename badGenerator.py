import random
import time
import csv

def generate_stream_data(throughput_per_second, duration):

    #Initializing global variables
    start_time = time.time()
    end_time = start_time + duration
    event_count, avg_throughput, total_events = 0,0,0
    file_counter=1
    eventList = []
    avg_throughputs = []
    timestamps=[]
    window_num=1

    #Starting infiite loop
    while time.time() <=end_time:
        timestamp = int(time.time())
        random_integer = random.randint(1, 10)
        random_char = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        # random_char = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

        #Create event
        event = {
            'timestamp': timestamp,
            'int': random_integer,
            'letter': random_char
        }
        eventList.append(event)

        event_count += 1

        # Check if a second has passed
        elapsed_time = time.time() - start_time
        if elapsed_time >= 1:
            #Calculate throughput for file
            actual_throughput = event_count / elapsed_time
            total_events+=event_count

            #Calculate running average throughput
            avg_throughput = total_events/file_counter
            
            # print(f'Throughput: {actual_throughput} tuples per second')
            print(f'Average Throughput of Generator: {avg_throughput} tuples per second\n')

            start_time = time.time()
            event_count = 0
            filename = f'data/{file_counter}.csv'
            # filename= 'stream_data.csv'
            # Writing events to csv file
            with open(filename, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['timestamp', 'int', 'letter'])
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerows(eventList)

            with open('stream_data.csv', mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['timestamp', 'int', 'letter'])
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerows(eventList)

            eventList = []
            file_counter+=1

        #Make generator sleep to allow specific throughput
        sleep_time = 1 / throughput_per_second
        time.sleep(sleep_time)

    return 0

if __name__ == "__main__":
    generate_stream_data(throughput_per_second=100,duration=5)