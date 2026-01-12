import time
import os
import shutil
from ascii2png.core import CoreService

def run_benchmark():
    test_dir = "bench_output"
    os.makedirs(test_dir, exist_ok=True)
    
    # Complex ASCII Diagram
    complex_text = """
    +-------------------+       +-------------------+
    |   Client          |       |   Server          |
    |                   |       |                   |
    |  +-------------+  |       |  +-------------+  |
    |  | Request     |--+------>|  | Processing  |  |
    |  +-------------+  |       |  +-------------+  |
    |                   |       |         |         |
    |  +-------------+  |       |  +-------------+  |
    |  | Response    |< +-------+--| Database    |  |
    |  +-------------+  |       |  +-------------+  |
    +-------------------+       +-------------------+
    """ * 10  # Repeat to make it larger
    
    start_time = time.time()
    iterations = 10
    
    print(f"Running benchmark with {iterations} iterations...")
    
    for i in range(iterations):
        CoreService.convert(
            text=complex_text,
            output_dir=test_dir,
            filename_hint=f"bench_{i}"
        )
        
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / iterations
    
    print(f"Total Time: {total_time:.4f}s")
    print(f"Average Time per Image: {avg_time:.4f}s")
    
    # Cleanup
    shutil.rmtree(test_dir)
    return avg_time

if __name__ == "__main__":
    run_benchmark()
