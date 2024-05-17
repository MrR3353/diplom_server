import sys
import time

# def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
#     """
#     Call in a loop to create a progress bar in the console.
#
#     :param iteration: Current iteration (Int)
#     :param total: Total iterations (Int)
#     :param prefix: Prefix string (Str)
#     :param suffix: Suffix string (Str)
#     :param decimals: Positive number of decimals in percent complete (Int)
#     :param length: Character length of bar (Int)
#     :param fill: Bar fill character (Str)
#     """
#     percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
#     filled_length = int(length * iteration // total)
#     bar = fill * filled_length + '-' * (length - filled_length)
#     sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
#     sys.stdout.flush()
#     if iteration == total:
#         sys.stdout.write('\n')
#
# # Example usage
# total_tasks = 3
# start = time.time()
# for i in range(1, total_tasks + 1):
#     time.sleep(0.5)
#     print_progress_bar(i, total_tasks, prefix='Progress:', suffix=f'Time: {time.time() - start}', length=30)


import sys
import time
import datetime

def print_progress_bar(iteration, total, start_time, prefix='', suffix='', decimals=1, length=50, fill='█'):
    """
    Call in a loop to create a progress bar in the console with a timer.

    :param iteration: Current iteration (Int)
    :param total: Total iterations (Int)
    :param start_time: Start time of the process (Datetime)
    :param prefix: Prefix string (Str)
    :param suffix: Suffix string (Str)
    :param decimals: Positive number of decimals in percent complete (Int)
    :param length: Character length of bar (Int)
    :param fill: Bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)

    # Calculate elapsed time
    elapsed_time = datetime.datetime.now() - start_time
    elapsed_seconds = elapsed_time.total_seconds()

    # Calculate estimated total time and remaining time
    if iteration > 0:
        estimated_total_time = elapsed_seconds * total / iteration
        remaining_time = estimated_total_time - elapsed_seconds
    else:
        remaining_time = 0

    elapsed_str = str(datetime.timedelta(seconds=int(elapsed_seconds)))
    remaining_str = str(datetime.timedelta(seconds=int(remaining_time)))

    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix} Elapsed: {elapsed_str} Remaining: {remaining_str}')
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')

# Example usage
total_tasks = 20
start_time = datetime.datetime.now()
for i in range(1, total_tasks + 1):
    time.sleep(0.2)
    print_progress_bar(i, total_tasks, start_time, prefix='Progress:', suffix='Complete', length=50)


# a = 1
# b = 1
# # bool
# print(1 < 2)
# print(a != b)
# c = False
#
# if 1 < 2:
#     print('abc')

# print('x y z')
# for x in range(2):
#     for y in range(2):
#         for z in range(2):
#             if ((x or y) <= (z == x)) == 1:
#                 print(x, y, z)
# 0 <= 0 = 1
# 0 <= 1 = 1
# 1 <= 0 = 0
# 1 <= 1 = 1
# (x <= (not y)) ∨ (y ≡ z) ∨ ¬w
# (x and y) <= z