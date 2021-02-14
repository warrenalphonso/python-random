"""
A naive classifier for handwritten digits. With the training data, we compute 
the average darkness for each of the 10 digits. Then we classify test data
by finding the number with the closest average darkness. 

This prefers `mnist_loader.load_data` so I'll just call it here instead of 
making it something I have to import into a Notebook and run. 
"""
import mnist_loader 

def avg_darknesses(training_data):
    digit_counts = {} 
    darknesses = {}
    for image, digit in zip(training_data[0], training_data[1]):
        digit_counts[digit] = 1 + digit_counts.get(digit, 0)
        darknesses[digit] = sum(image) + darknesses.get(digit, 0)
    avgs = {} 
    for digit, n in digit_counts.items():
        avgs[digit] = darknesses[digit] / n 
    return avgs 

def guess_digit(image, avgs):
    darkness = sum(image)
    distances = { k: abs(v - darkness) for k, v in avgs.items() }
    return min(distances, key=distances.get)

if __name__ == "__main__":
    training_data, validation_data, test_data = mnist_loader.load_data()
    # Training phase 
    avgs = avg_darknesses(training_data) 
    # Testing phase: see how many we classify correctly 
    num_correct = sum(guess_digit(image, avgs) == digit 
            for image, digit in zip(test_data[0], test_data[1]))
    print("{} of {} values correct.".format(num_correct, len(test_data[1])))
