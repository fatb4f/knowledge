# Runtime Guide

This directory holds optional runtime ingress adapters for the generated contract family.

## Purpose

- parse runtime config at the Python boundary
- validate against generated schema references
- emit normalized config and structured errors

## Rules

- runtime adapters are not the source of truth
- reject unknown keys by default
- do not silently normalize by dropping data
- keep adapter behavior narrower than the contract family
