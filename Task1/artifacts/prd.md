## Overview
- The website lets users enter a city, address, or landmark and generates a custom horror story tied to that location plus a matching AI image.  
- The results page displays the story text and image together with actions to copy, download, and share.  
- An admin dashboard allows moderators to review generation logs, handle user reports, and remove or block problematic content.  

## Goals
- Provide a fast location-to-story experience with autosuggest location input and a single “Generate” action.  
- Support creator workflows with selectable story length and tone and high-resolution image downloads.  
- Reduce unsafe outputs by applying moderation filters, user reporting, and moderator tools for takedown and blocking.  

## Non-Goals
- The product will not provide real-time navigation, maps, or routing beyond validating and normalizing the entered location string.  
- The product will not guarantee factual historical accuracy about a location and will label outputs as fictional.  
- The product will not support user accounts at launch, so saved libraries and cross-device sync are out of scope.  

## User Personas (brief)
- Casual Reader needs an autosuggest location field, a clear “Generate” button, and one-click share/download of the story and image.  
- Travel Blogger needs story length and tone controls plus copy-to-clipboard text and high-resolution image downloads for publishing.  
- Moderator needs an admin dashboard with generation logs, user reports, content removal, blocked inputs, and safe-regeneration tools.  

## Key Features
- Location entry with autocomplete suggestions, geocoding normalization, and validation errors for invalid or ambiguous inputs.  
- Story controls including length presets (e.g., 300/800/1500 words) and tone presets (e.g., local folklore, modern, psychological).  
- Results view showing the generated story, a single featured image, and buttons for copy text, download image, and share link.  
- Admin dashboard with searchable logs, report queue, content hide/delete, blocked location/prompt rules, and “regenerate with safe mode” action.  

## User Flows
- User types a location, selects an autosuggested option, chooses length/tone (optional), and clicks “Generate” to start generation.  
- System shows a progress state, then renders the story and image with copy/download/share actions on the results page.  
- User clicks “Report” on a result, selects a reason, adds optional notes, and submits a report tied to the generation ID.  
- Moderator opens the admin queue, reviews flagged items with prompts/outputs, then hides/deletes content and optionally blocks the triggering input.  

## Functional Requirements
- The location field must call a geocoding service to return up to 5 suggestions and store the chosen place name plus lat/long.  
- The generation endpoint must accept location, length, tone, and a safety flag, then return story text, image URL, and a generation ID.  
- The results page must support copy-to-clipboard for story text and image download as PNG at 1024×1024 and 2048×2048 when available.  
- The admin dashboard must allow searching by generation ID, viewing the prompt/output metadata, and performing hide/delete/block/regenerate actions.  

## Non-Functional Requirements
- The “Generate” action must return a completed story and image within 20 seconds for p95 requests under normal load.  
- The site must meet WCAG 2.1 AA with keyboard navigation, visible focus states, and alt text for generated images.  
- All generated content and reports must be logged with timestamps and hashed IP identifiers for abuse analysis without storing raw IPs.  
- The system must enforce rate limits of 10 generations per hour per hashed IP and show a clear throttling message when exceeded.  

## Constraints/Assumptions
- Story generation and image generation will use third-party AI APIs that may impose content policies and rate limits.  
- The location autosuggest will rely on an external geocoding provider and may return incomplete results for rural areas.  
- Without user accounts, share links will be the primary persistence mechanism and will expire after 30 days unless flagged or pinned by admins.  

## Success Metrics
- At least 60% of sessions that enter a location reach a successful generation completion within one attempt.  
- Median time from clicking “Generate” to viewing results is under 12 seconds across all devices.  
- At least 25% of successful generations result in a copy, download, or share action within the same session.  
- Fewer than 1% of generations are removed by moderators for policy violations after safety filters are applied.  

## Open Questions
- Which geocoding provider (e.g., Google Places, Mapbox, OpenStreetMap/Nominatim) best meets cost and usage constraints for autosuggest?  
- What image aspect ratio(s) are required for target sharing destinations (e.g., 1:1, 4:5, 16:9) and which should be supported at launch?  
- What specific safety policy categories should be blocked automatically versus routed to manual review in the moderator queue?  
- Should share links be publicly indexable or protected via unguessable tokens with no SEO indexing by default?