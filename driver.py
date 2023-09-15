import time
import threading
import consumer
import generator
import matplotlib.pyplot as plt
import os
from matplotlib.ticker import MaxNLocator

regex_pattern = r'AB'
window_duration = 10
driver_duration = 200
gen_throughput = 10000
file_lock = threading.Lock()
if not os.path.exists("data"):
    os.makedirs("data")

consumer_event = threading.Event()
generator_event = threading.Event()

consumer_result = None
generator_result = None

def run_consumer():
    global consumer_result
    consumer_result = consumer.find_pattern_in_window(regex_pattern, window_duration, driver_duration, gen_throughput)
    # consumer_result = badConsumer.find_pattern_in_window(regex_pattern, window_duration, driver_duration, 10, gen_throughput)
    consumer_event.set()  # Signal that the consumer thread is done

def run_generator():
    global generator_result
    generator_result = generator.generate_stream_data(gen_throughput, driver_duration, file_lock, window_duration)
    generator_event.set()  # Signal that the generator thread is done

consumer_thread = threading.Thread(target=run_consumer)
generator_thread = threading.Thread(target=run_generator)

consumer_thread.start()
generator_thread.start()

consumer_thread.join()
generator_thread.join()

print(consumer_result[2])
print(generator_result[1])
plt.figure(figsize=(10, 6))
plt.plot(generator_result[0], generator_result[2], label='Generator Througput')
plt.plot(consumer_result[0], consumer_result[2], label='Consumer Througput')

plt.xlabel('Window')
plt.ylabel('Throughput')
plt.legend()
plt.title('Total Events and Average Throughput Over Time')
plt.grid(True)
plt.savefig('plot.png')
plt.show()
