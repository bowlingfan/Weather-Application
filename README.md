# Weather-Application
Creation of a basic Weather Application, with some quirks inspired by [CARROT](https://www.meetcarrot.com/weather/), a companion-based weather mobile application with some humor added as personality. Weather Application was created using Python with QT6, API calls from [National Weather Service](https://www.weather.gov/) (NWS) and [Geocode-xyz](https://geocode.xyz/), and SQL. Features include:
- Selecting a location (Which can be saved!)
- Getting weather data at the "current" moment
- Forecasting weather for the next 7 days
- Showing warnings in the selected location if existent

## Notes
Only locations in the United States are valid for this program; any other locations outside of the US will not be accepted (due to NWS only providing data in the US)
Incomplete project. If you receive an error stating, `Weather data could not be retrieved. Please try again after one second.`, then the API call is throttled and you'll have to retry again, as one API I use (geocode-xyz) has strict limits. The state names may not always be accurate and naming can be inconsistent with cities, this comes from issues with API, Geocode-xyz.

<img width="865" height="476" alt="designing" src="https://github.com/user-attachments/assets/82981670-382f-4296-b520-bad7d5770129" />

## Credits
* [QT](https://www.qt.io/), a package meant for creating User Interfaces.
* [CARROT](https://www.meetcarrot.com/weather/), the inspiration to make this application.
* [National Weather Service](https://www.weather.gov/), for providing real-time weather data and forecasting data.
* [Geocode-xyz](https://geocode.xyz/), for converting location data into a geological position usable by NWS.
