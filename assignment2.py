#!/usr/bin/env python3

"""
OPS445 Assignment 2 - Summer 2026
Program: assignment2.py
Author: David Brand
The python code in this file is original work written by
David Brand. No code in this file is copied from any other source
except those provided by the course instructor, including any person,
textbook, or on-line resource. I have not shared this python script
with anyone or anything except for submission for grading.
I understand that the Academic Honesty Policy will be enforced and
violators will be reported and appropriate action will be taken.

Description: Displays system memory information using text-based bar graphs.

Date: 2026-07-17
"""

import argparse
import os
import sys


def parse_command_args() -> object:
    """Set up and return the command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Memory Visualiser -- See Memory Usage Report with bar charts"
        ),
        epilog="Copyright 2023"
    )
    parser.add_argument(
        "-H",
        "--human-readable",
        action="store_true",
        help="Display memory values in human-readable format."
    )
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=20,
        help="Specify the length of the graph. Default is 20."
    )
    parser.add_argument(
        "program",
        type=str,
        nargs="?",
        help=(
            "If a program is specified, show memory use of all associated "
            "processes. Show only total use if not."
        )
    )
    return parser.parse_args()


def percent_to_graph(percent: float, length: int = 20) -> str:
    """Turn a percentage from 0.0 to 1.0 into a text bar graph."""
    filled_length = round(percent * length)
    empty_length = length - filled_length
    return "#" * filled_length + " " * empty_length


def get_sys_mem() -> int:
    """Return the total system memory in kB."""
    with open("/proc/meminfo", "r") as meminfo:
        for line in meminfo:
            if line.startswith("MemTotal:"):
                return int(line.split()[1])
    return 0


def get_avail_mem() -> int:
    """Return the total memory currently available in kB."""
    with open("/proc/meminfo", "r") as meminfo:
        for line in meminfo:
            if line.startswith("MemAvailable:"):
                return int(line.split()[1])
    return 0


def pids_of_prog(app_name: str) -> list:
    """Return a list of process IDs associated with an application."""
    pid_output = os.popen(f"pidof {app_name}").read()
    return pid_output.split()


def rss_mem_of_pid(proc_id: str) -> int:
    """Return the total resident memory used by one process in kB."""
    rss_total = 0
    smaps_path = f"/proc/{proc_id}/smaps"

    with open(smaps_path, "r") as smaps:
        for line in smaps:
            if line.startswith("Rss:"):
                rss_total += int(line.split()[1])

    return rss_total


def bytes_to_human_r(kibibytes: int, decimal_places: int = 2) -> str:
    """Turn 1,024 KiB into 1 MiB, for example."""
    suffixes = ["KiB", "MiB", "GiB", "TiB", "PiB"]
    suf_count = 0
    result = kibibytes

    while result > 1024 and suf_count < len(suffixes) - 1:
        result /= 1024
        suf_count += 1

    str_result = f"{result:.{decimal_places}f} "
    str_result += suffixes[suf_count]
    return str_result


if __name__ == "__main__":
    args = parse_command_args()
    if not args.program:
        pass
    else:
        pass
