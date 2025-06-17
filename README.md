# Program Builder

> Build and export structured event programs with multi-day, multi-stage support — export to clean HTML in ③ easy steps.

---

## Source Code

[![GitHub][github-badge]][source]

[source]: https://github.com/nodes-ro/program-builder.git  
[github-badge]: https://img.shields.io/badge/GitHub-Source%20Code-blue?logo=github

---

## Problem / Solution

**Problem:** Manually crafting event programs and embedding them into a webpages is tedious, often requiring spreadsheets or design tools followed by hand-coding HTML.

**Solution:** A free, lightweight, Docker-deployable web app with an easy wizard that guides you through defining days, time slots, stages, and events—then exports a polished HTML schedule in just three steps.

---

## Key Features

- **Multi-Day Support:** Create schedules spanning any number of days.  
- **Multi-Stage Layout:** Organize concurrent sessions across multiple stages or tracks.  
- **Custom Intervals:** Choose slot lengths (60, 30, 15, or 10 minutes) to fit your timetable.  
- **Event Details & Thumbnails:** Add titles, descriptions, and optional image URLs for each session.  
- **Styles:** Apply Pico.css table themes like striped or default for readability.  
- **Export to HTML:** Download a standalone HTML file preloaded for seamless integration.

---

## Support us

Join us on our journey:

- **Donate** 
- **Spread the Word:** Share with friends, teams, or communities.  
- **Provide Feedback:** Let us know your suggestions or report issues.  

---

## Demo

- **Live Demo:** https://program-builder.nodes.ro

---

## Build & Run Docker Image

### 1. Remove any existing image
> docker rmi -f program-builder:0.0.1

### 2. Build the new image (must be run from the directory containing your Dockerfile)
> docker build -t program-builder:0.0.1 .

### 3. Run the container
> docker run -d -p 8010:8010 program-builder:0.0.1

