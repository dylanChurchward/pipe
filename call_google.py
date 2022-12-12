import time
import math
import requests

# number of times you want to call the FaaS 
function_calls = 10

# store the runtime of each FaaS function call 
runtimes = []

# the json you want to send to your FaaS 
json = '{"name": "bug.jpg","radius": 5,"width": 500,"height": 700,"enhanced": 3,"rotate": 180}'

# call the FaaS function
def call_function():
    url = "https://image-processing-ikxu3nztsq-ue.a.run.app"
    payload = json
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    #response.elapsed.total_seconds()
    
# call the FaaS once before collecting runtime data, so the cold start doesn't skew the data 
call_function()                         

for x in range(0, function_calls, 1):
    start = time.time()
    call_function()
    finish = time.time()
    runtimes.append(finish - start)
    print(runtimes[x]) # make sure its working 

# find average runtime 
total = 0
for x in runtimes: 
    total = total + x

average_runtime = total / len(runtimes)

print("average runtime:", average_runtime)

# find the standard deviation of runtime 
sum_of_squares = 0
for x in runtimes:
    sum_of_squares = sum_of_squares + pow(abs(x - average_runtime), 2)

standard_deviation = math.sqrt(sum_of_squares / len(runtimes))
print("standard deviation of runtimes", standard_deviation)

# find Coefficient of Variation
coefficient_of_variation = (standard_deviation / average_runtime) * 100;
print("coefficient of variation", coefficient_of_variation)