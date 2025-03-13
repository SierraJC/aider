#!/usr/bin/env python3
import json
import os
import re
import sys

import pyte

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} input_cast_file output_cast_file")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Initialize pyte screen and stream
    screen = pyte.Screen(80, 24)
    stream = pyte.Stream(screen)
    
    # Read and parse the cast file
    with open(input_file, 'r') as f:
        # First line is header
        header = f.readline().strip()
        
        # Read the events
        events = [json.loads(line) for line in f if line.strip()]
    
    filtered_events = []
    
    # Process each event through the terminal emulator
    for event in events:
        # Process the event in the terminal
        if len(event) >= 3 and event[1] == 'o':  # Output event
            stream.feed(event[2])
            
            # Check if "Atuin" is visible on screen
            display_content = "\n".join("".join(line) for line in screen.display)
            if "Atuin" in display_content:
                continue  # Skip this event
        
        # Keep this event
        filtered_events.append(event)
    
    # Write the filtered content to the output file
    with open(output_file, 'w') as f:
        f.write(header + '\n')
        for event in filtered_events:
            f.write(json.dumps(event) + '\n')

if __name__ == "__main__":
    main()
