import sys
import csv
import math
import hashlib


# Function to read and extract data from csv
def csvReader(filename):
    data = []

    # Open file and store all data in list
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader) # Skip the first line (header)

        for line in reader:
            data.append(line)
    
    return data



# Function to populate bloom filter
def bloomFilter(data, m, k):
    bloomFilter = [0] * m

    for element in data:
        addElement(bloomFilter, k, str(element)[2:-2]) # Slicing is done to remove brackets and single quotes

    return bloomFilter



# Function to add element to bloom filter
def addElement(bloomFilter, k, elem):
    for i in range(k):
        # Create hash value for the element
        hashObj = hashlib.sha256((elem + str(i)).encode())
        hashVal = int(hashObj.hexdigest(), 16)
        
        # Calculate position in bloom filter and set value at position to 1
        pos = hashVal % bloomFilter.__len__()
        bloomFilter[pos] = 1



# Function to check if element might be present in bloom filter
def check(bloomFilter, k, elem):
    for i in range(k):
        # Create hash value for the element and calculate position in bloom filter
        hashObj = hashlib.sha256((elem + str(i)).encode())
        hashVal = int(hashObj.hexdigest(), 16)
        pos = hashVal % bloomFilter.__len__()
        
        # If value at calculated position equals 0, element is not present
        if bloomFilter[pos] == 0:
            print(elem + ",Not in the DB")
            return False
        
    print(elem + ",Probably in the DB")
    return True



# Main function to run everything
def main():
    if len(sys.argv) > 1:
        # Get CSV files from command line argument and save their data in lists
        dataFile = sys.argv[1]
        testData = csvReader(dataFile)

        emails = sys.argv[2]
        testEmails = csvReader(emails)

        # Initialize and calculate necessary values to create bloom filter
        p = 0.0000001 # probability of false positives
        n = testData.__len__() # number of items in filter
        m = math.ceil((n * math.log(p)) / math.log(1 / pow(2, math.log(2)))) # number of bits in filter
        k = round((m / n) * math.log(2)) # number of hash functions

        # Initialize and populate bloom filter with emails from first input file
        bf = bloomFilter(list(testData), m, k)
        
        # Check if emails from second input file might be present in bloom filter
        for email in testEmails:
            check(bf, k, str(email)[2:-2])


# This condition prevents the script from running unless it's executed directly
if __name__ == "__main__":
    main()

