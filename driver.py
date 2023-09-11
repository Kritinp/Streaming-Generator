import time
import threading
import consumer
import generator
import matplotlib.pyplot as plt
# import matplotlib

# matplotlib.use('SVG')

regex_pattern = r'AB'
window_duration = 1
driver_duration = 10
gen_throughput = 10000

consumer_event = threading.Event()
generator_event = threading.Event()

consumer_result = None
generator_result = None

def run_consumer():
    global consumer_result
    consumer_result = consumer.find_pattern_in_window(regex_pattern, window_duration, driver_duration)
    consumer_event.set()  # Signal that the consumer thread is done

def run_generator():
    global generator_result
    generator_result = generator.generate_stream_data(gen_throughput, driver_duration)
    generator_event.set()  # Signal that the generator thread is done

consumer_thread = threading.Thread(target=run_consumer)
generator_thread = threading.Thread(target=run_generator)

consumer_thread.start()
generator_thread.start()

consumer_thread.join()
generator_thread.join()

plt.figure(figsize=(10, 6))
plt.plot(consumer_result[0], consumer_result[1], label='Total Events')
plt.plot(consumer_result[0], consumer_result[2], label='Average Throughput')
plt.xlabel('Time (seconds)')
plt.ylabel('Count/Throughput')
plt.legend()
plt.title('Total Events and Average Throughput Over Time')
plt.grid(True)
plt.savefig('plot.png')
plt.show()
