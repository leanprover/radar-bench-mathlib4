#!/usr/bin/env python3

import argparse
import json
import os
import resource
import subprocess
import sys
import tempfile
from dataclasses import dataclass


def print_result(metric: str, value: float, unit: str | None = None) -> None:
    data = {"metric": metric, "value": value}
    if unit is not None:
        data["unit"] = unit
    print(f"radar::measurement={json.dumps(data)}")


@dataclass
class PerfMetric:
    event: str
    factor: float = 1
    unit: str | None = None


@dataclass
class RusageMetric:
    name: str
    factor: float = 1
    unit: str | None = None


PERF_METRICS = {
    "task-clock": PerfMetric("task-clock", 1e-9, "s"),
    "wall-clock": PerfMetric("duration_time", 1e-9, "s"),
    "instructions": PerfMetric("instructions"),
}

RUSAGE_METRICS = {
    "maxrss": RusageMetric("ru_maxrss", 1000, "b"),  # KiB on linux
}


def measure_perf(cmd: list[str], events: list[str]) -> dict[str, float]:
    with tempfile.NamedTemporaryFile() as tmp:
        cmd = [
            *["perf", "stat", "-j", "-o", tmp.name],
            *[arg for event in events for arg in ["-e", event]],
            *["--", *cmd],
        ]

        # Execute command
        env = os.environ.copy()
        env["LC_ALL"] = "C"  # or else perf may output syntactically invalid json
        result = subprocess.run(cmd, env=env)
        if result.returncode != 0:
            sys.exit(result.returncode)

        # Collect results
        perf = {}
        for line in tmp:
            data = json.loads(line)
            if "event" in data and "counter-value" in data:
                perf[data["event"]] = float(data["counter-value"])

        return perf


@dataclass
class Result:
    metric: str
    value: float
    unit: str | None


def measure(cmd: list[str], metrics: list[str]) -> list[Result]:
    # Check args
    unknown_metrics = []
    for metric in metrics:
        if metric not in RUSAGE_METRICS and metric not in PERF_METRICS:
            unknown_metrics.append(metric)
    if unknown_metrics:
        raise Exception(f"unknown metrics: {', '.join(unknown_metrics)}")

    # Prepare perf events
    events: list[str] = []
    for metric in metrics:
        if info := PERF_METRICS.get(metric):
            events.append(info.event)

    # Measure
    perf = measure_perf(cmd, events)
    rusage = resource.getrusage(resource.RUSAGE_CHILDREN)

    # Extract results
    results = []
    for metric in metrics:
        if info := PERF_METRICS.get(metric):
            value = perf.get(info.event)
            if value is None:
                # Without the corresponding permissions,
                # we only get access to the userspace versions of the counters.
                value = perf[f"{info.event}:u"]
            value *= info.factor
            results.append(Result(metric, value, info.unit))

        if info := RUSAGE_METRICS.get(metric):
            value = getattr(rusage, info.name) * info.factor
            results.append(Result(metric, value, info.unit))

    return results


def main(topics: list[str], metrics: list[str], cmd: list[str]):
    for result in measure(cmd, metrics):
        for topic in topics:
            print_result(f"{topic}//{result.metric}", result.value, result.unit)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--topic", action="append", default=[])
    parser.add_argument("-m", "--metric", action="append", default=[])
    parser.add_argument("cmd", nargs="*")
    args = parser.parse_args()
    main(args.topic, args.metric, args.cmd)
