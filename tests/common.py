import os
import os.path

def create_test_file(csv_file_path, supported_field, dataset):
    # Delete old file
    if os.path.isfile(csv_file_path):
        os.remove(csv_file_path)

    # Create tested file
    with open(csv_file_path, "a") as f:
        # Create the header
        f.write(";".join(supported_field))
        f.write("\n")

        # Fill the file with data from <dataset>
        for line in dataset:
            f.write("{}\n".format(line))