# Utils Image Bootstrap Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Bootstrap a fresh `avtools-docker` repo with a CPU-first Ubuntu 24.04 media-utils image layout suitable for later CPU/GPU matrix builds.

**Architecture:** Start with a narrow repo: one CPU Dockerfile, one Makefile, one smoke script, and a README that documents build arguments and mounted-volume conventions. Do not bake project app code into the image. Treat upstream tools as source fetch/build inputs and keep the runtime image as a reusable media/tooling substrate.

**Tech Stack:** Docker, Ubuntu 24.04 LTS, shell scripts, Make
