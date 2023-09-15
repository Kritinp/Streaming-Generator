import random
import time
import csv

def generate_stream_data(throughput_per_second, duration,file_lock, window_duration):

    # Initializing global variables
    start_time = time.time()
    end_time = start_time + duration
    event_count, avg_throughput, total_events, window_counter = 0, 0, 0, 0
    file_counter = 1
    eventList = []
    event_counts = []
    avg_throughputs = []
    timestamps=[]
    window_num=1
    # Starting infinite loop
    while time.time() <= end_time:
        loop_start = time.time()
        for i in range(throughput_per_second):

            if time.time() - loop_start > 0.5:
                print(f'Bottlenecked!!')
                break


            timestamp = int(time.time())
            random_integer = random.randint(1, 10)
            random_char = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

            # Create event
            event = {
                'timestamp': timestamp,
                'int': random_integer,
                'letter': random_char
            }
            eventList.append(event)
            event_count += 1

        # Writing to the file
        filename = f'data/{file_counter}.csv'

        with file_lock:
            with open(filename, mode='a', newline='') as file:
                print(f'Generating file {filename}\n')
                window_counter+=1
                writer = csv.DictWriter(file, fieldnames=['timestamp', 'int', 'letter'])
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerows(eventList)

        total_events += event_count
        if window_counter == window_duration:
            print(f'adding {total_events}')
            avg_throughput = total_events / window_duration
            event_counts.append(event_count)
            avg_throughputs.append(avg_throughput)
            timestamps.append(window_num)
            window_num+=1
            print(f'Average Throughput of Generator: {avg_throughput} tuples per second\n')
            total_events, window_counter = 0, 0

        event_count = 0
        eventList = []
        file_counter += 1

        loop_end = time.time()
        loop_duration = loop_end - loop_start
        if 1 - loop_duration > 0:
            time.sleep(1 - loop_duration)

    return [timestamps, event_counts, avg_throughputs]

if __name__ == "__main__":
    generate_stream_data(throughput_per_second=900000, duration=5)
