The storm data is structured across **three separate files that are linked by the event ID number**. These files provide different categories of information related to storm events: details, locations, and fatalities.

Here is a detailed recap of the structure of each file:

**1. Event Details File (StormEvents_details-ftp_v1.0_dYYYY_cYYYYMMDD.csv):**

This file contains comprehensive information about individual storm events within storm episodes. Each row in this file represents a unique storm event identified by a specific `event_id`. Key fields in this file include:

*   **Temporal Information**:
    *   `begin_yearmonth`: The year and month the event began (YYYYMM format).
    *   `begin_day`: The day of the month the event began (DD format).
    *   `begin_time`: The time of day the event began (hhmm format).
    *   `end_yearmonth`: The year and month the event ended (YYYYMM format).
    *   `end_day`: The day of the month the event ended (DD format).
    *   `end_time`: The time of day the event ended (hhmm format).
    *   `year`: The four-digit year of the event.
    *   `month_name`: The name of the month of the event (spelled out).
    *   `begin_date_time`: The start date and time of the event in MM/DD/YYYY hh:mm:ss format (usually in LST).
    *   `end_date_time`: The end date and time of the event in MM/DD/YYYY hh:mm:ss format (usually in LST).
*   **Event Identification and Context**:
    *   `episode_id`: A unique ID assigned by the NWS to a storm episode, which can contain multiple individual events.
    *   `event_id`: A unique ID assigned by the NWS for each individual storm event. This is the **primary key that links records across the three files**.
    *   `state`: The name of the state where the event occurred (in ALL CAPS).
    *   `state_fips`: A unique number assigned to the state by NIST.
    *   `event_type`: The type of weather event (spelled out), as defined in NWS Directive 10-1605. Permitted event types include 'Hail', 'Thunderstorm Wind', 'Snow', 'Ice', 'Tornado', etc..
*   **Location Information (at a higher level than the Location File)**:
    *   `cz_type`: Indicates if the event occurred in a County/Parish (C), NWS Public Forecast Zone (Z), or Marine area (M).
    *   `cz_fips`: The FIPS number for the county or the NWS Forecast Zone Number.
    *   `cz_name`: The name of the County/Parish, Zone, or Marine area.
    *   `wfo`: The National Weather Service Forecast Office's area of responsibility.
    *   `cz_timezone`: The time zone for the County/Parish, Zone, or Marine Name (e.g., EST-5, CST-6).
*   **Impact Information**:
    *   `injuries_direct`: The number of direct injuries caused by the event.
    *   `injuries_indirect`: The number of indirect injuries caused by the event.
    *   `deaths_direct`: The number of direct deaths caused by the event.
    *   `deaths_indirect`: The number of indirect deaths caused by the event.
    *   `damage_property`: The estimated property damage (e.g., 10.00K, 10.00M). 'K' represents thousands of dollars, and 'M' represents millions of dollars.
    *   `damage_crops`: The estimated crop damage (e.g., 0.00K, 15.00M).
*   **Event Details**:
    *   `source`: The source reporting the event (e.g., Public, Newspaper, Trained Spotter).
    *   `magnitude`: The measured extent of the magnitude type (e.g., wind speed in knots, hail size in inches).
    *   `magnitude_type`: The type of magnitude measured (e.g., Estimated Gust (EG), Measured Sustained Wind (MS)).
    *   `flood_cause`: The reported or estimated cause of a flood (e.g., Ice Jam, Heavy Rain).
    *   `category`: This field was unknown at the time of the documentation.
    *   `tor_f_scale`: The Enhanced Fujita Scale for tornadoes (EF0-EF5).
    *   `tor_length`: The length of the tornado on the ground (in miles).
    *   `tor_width`: The width of the tornado on the ground (in yards).
    *   Fields related to continuing tornado segments across different WFOs, states, and counties (`tor_other_wfo`, `tor_other_cz_state`, `tor_other_cz_fips`, `tor_other_cz_name`).
    *   `begin_range`, `begin_azimuth`, `begin_location`: Details about the starting point of the event or damage path relative to a named location.
    *   `end_range`, `end_azimuth`, `end_location`: Details about the ending point of the event or damage path relative to a named location.
    *   `begin_lat`: The latitude of the event's starting point.
    *   `begin_lon`: The longitude of the event's starting point.
    *   `end_lat`: The latitude of the event's ending point.
    *   `end_lon`: The longitude of the event's ending point.
    *   `episode_narrative`: A general description of the overall storm episode created by the NWS.
    *   `event_narrative`: Descriptive details of the individual event created by the NWS.

**2. Storm Data Location File (StormEvents_locations-ftp_v1.0_dYYYY_cYYYYMMDD.csv.gz):**

This file provides specific location details for events recorded in the Event Details File. An event can have multiple locations associated with it, each with a unique `location_index`. Key fields include:

*   `episode_id`: Links back to the storm episode in the Event Details File.
*   `event_id`: Links back to the specific storm event in the Event Details File.
*   `location_index`: A sequential number assigned to specific locations within the same storm event.
*   `range`: Distance to the geographical center or primary post office of a named location (in miles).
*   `azimuth`: The 16-point compass direction from the referenced location.
*   `location`: The name of the city, town, or village used as a reference point for range and azimuth.
*   `lat`: The latitude where the event occurred.
*   `lon`: The longitude where the event occurred.

**3. Storm Data Fatality File (StormEvents_fatalities-ftp_v1.0_dYYYY_cYYYYMMDD.csv.gz):**

This file contains information about fatalities (both direct and indirect) caused by storm events. Each row represents a single fatality associated with a specific event. Key fields include:

*   `fatality_id`: A unique ID assigned to each individual fatality.
*   `event_id`: Links back to the specific storm event in the Event Details File.
*   `fatality_type`: Indicates whether the fatality was direct (D) or indirect (I), as determined by NWS software.
*   `fatality_date`: The date and time of the fatality (usually time is 00:00).
*   `fatality_age`: The age of the deceased (can be 'null' if unknown).
*   `fatality_sex`: The gender of the deceased (can be 'null' if unknown).
*   `fatality_location`: A code indicating the location where the fatality occurred (e.g., UT for Under Tree, VE for Vehicle).

In summary, the data is structured with a central **Event Details File** containing core information about each storm event. This file is linked to the **Storm Data Location File** via the `event_id` to provide more granular spatial information about the event. Similarly, the **Storm Data Fatality File** is also linked to the Event Details File using the `event_id` to record details about fatalities associated with those events. This relational structure allows for a comprehensive understanding of storm events, their locations, and their impacts on human life.