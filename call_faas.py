import boto3
import time
import math

# number of times you want to call the FaaS 
function_calls = 3

# store the runtime of each FaaS function call 
runtimes = []

# the json you want to send to your FaaS 
json = '{"bucketname": "image.bucket.tcss462562-2","rotate": "180","width": "500","height": "700","enhanced": "2","radius": "4"}'

# call the FaaS function
def call_function():
    lambda_client = boto3.client('lambda')
    lambda_client.invoke(FunctionName='image-pipeline', 
                         InvocationType='RequestResponse',
                         Payload=json)
    
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
