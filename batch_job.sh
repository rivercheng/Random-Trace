#!/bin/bash
python traceGenerator.py data.db.pickle 10000 output_trace/behavior
python readtrace.py output_trace/ output.db
python analyze.py output.db > output.random
