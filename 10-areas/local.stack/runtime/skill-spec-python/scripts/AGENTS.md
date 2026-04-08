# Scripts Guide

This directory contains deterministic helpers invoked by the bounded workflow.

## Rules

- keep scripts side-effect scoped to `generated/`
- do not encode semantic contract meaning here
- prefer stable JSON reports and deterministic output ordering
